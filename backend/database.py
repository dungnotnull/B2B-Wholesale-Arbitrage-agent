from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from backend.config import settings

Base = declarative_base()

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    platform = Column(String) # 1688, Alibaba
    platform_id = Column(String, unique=True)
    location = Column(String)
    rating = Column(Float)
    years_active = Column(Integer)
    trust_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    negotiations = relationship("Negotiation", back_populates="supplier")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    sku = Column(String, unique=True)
    title = Column(String)
    image_url = Column(String)
    embedding = Column(Text) # Store as JSON string or use PGVector in future
    category = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Negotiation(Base):
    __tablename__ = "negotiations"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    status = Column(String) # In-progress, Completed, Failed
    current_price = Column(Float)
    target_price = Column(Float)
    moq = Column(Integer)
    transcript = Column(Text) # AES-256 Encrypted JSON
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    supplier = relationship("Supplier", back_populates="negotiations")

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
