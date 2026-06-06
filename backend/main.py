import os
from cryptography.fernet import Fernet
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from backend.database import SessionLocal, init_db, Supplier, Product, Negotiation
from backend.core_loop import SourcingCoreLoop
from backend.config import settings

# Initialize DB
init_db()

app = FastAPI(title="B2B Wholesale Arbitrage API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key_header = APIKeyHeader(name="X-API-KEY")

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != "super-secret-prod-key":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Invalid API Key"
        )
    return api_key

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Security Layer for encrypted logs
cipher_suite = Fernet(os.getenv("ENCRYPTION_KEY", Fernet.generate_key()))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}

@app.post("/api/v1/source", dependencies=[Depends(verify_api_key)])
async def source_product(image_url: str, quantity: int, target_price: float, db: Session = Depends(get_db)):
    core = SourcingCoreLoop()
    # Use the provided image_url (or a temporary local path if uploaded)
    results = await core.run_sourcing_pipeline(image_url, quantity, target_price)
    
    # Store findings in DB
    for supplier in results["top_suppliers"]:
        db_supplier = Supplier(
            name=supplier["title"], 
            rating=supplier["rating"],
            platform="1688"
        )
        db.add(db_supplier)
    db.commit()
    
    return results

@app.post("/api/v1/negotiate", dependencies=[Depends(verify_api_key)])
async def start_negotiation(supplier_id: str, script: str, db: Session = Depends(get_db)):
    # Encrypt the script before saving to DB for privacy
    encrypted_script = cipher_suite.encrypt(script.encode()).decode()
    
    neg = Negotiation(
        supplier_id=supplier_id,
        transcript=encrypted_script,
        status="In-progress"
    )
    db.add(neg)
    db.commit()
    
    return {"status": "started", "negotiation_id": neg.id}
