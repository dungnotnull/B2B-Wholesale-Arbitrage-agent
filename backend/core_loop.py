import asyncio
from typing import List, Dict, Any
from backend.vision_scraper import VisionProvider, ScraperProvider, GoogleVisionProvider, LocalCLIPProvider, PlaywrightScraper
from backend.llm_broker import LLMBroker, NegotiationContext, ClaudeBackend, OpenAIBackend, OllamaBackend
from backend.database import SessionLocal, Product, Supplier, Negotiation
from backend.config import settings
import numpy as np

class SourcingCoreLoop:
    def __init__(self):
        self.vision = GoogleVisionProvider(settings.google_vision_api_key)
        self.clip = LocalCLIPProvider(settings.clip_model_id)
        self.scraper = PlaywrightScraper()
        self.broker = LLMBroker([
            ClaudeBackend(settings.claude_api_key),
            OpenAIBackend(settings.openai_api_key),
            OllamaBackend(settings.ollama_model)
        ])

    async def run_sourcing_pipeline(self, query_image_path: str, target_quantity: int, target_price: float):
        # 1. Reverse Image Search
        web_results = await self.vision.reverse_image_search(query_image_path)
        
        # 2. Extract Data
        scraped_products = []
        for res in web_results:
            data = await self.scraper.extract_product_data(res["url"])
            if "error" not in data:
                scraped_products.append(data)
            
        # 3. Local CLIP Re-ranking
        query_embedding = await self.clip.get_image_embedding(query_image_path)
        
        final_ranked_list = []
        for prod in scraped_products:
            # Real implementation: download image, get embedding, compute cosine similarity
            prod_embedding = await self.clip.get_image_embedding(prod["image_url"])
            similarity = np.dot(query_embedding, prod_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(prod_embedding))
            prod["similarity_score"] = float(similarity)
            final_ranked_list.append(prod)

        # Rank by (Similarity * 0.6 + Rating * 0.4)
        final_ranked_list.sort(key=lambda x: (x["similarity_score"] * 0.6 + (x["rating"]/5 * 0.4)), reverse=True)
        
        # 4. Top 5 & Negotiation Script
        top_5 = final_ranked_list[:5]
        best_match = top_5[0] if top_5 else None
        
        script = ""
        if best_match:
            context = NegotiationContext(
                product_id=best_match.get("title", "unknown"),
                user_intent="Request factory direct price and MOQ flexibility",
                target_price=target_price,
                quantity=target_quantity,
                history=[],
                language_target="zh"
            )
            script = await self.broker.negotiate(context)
        
        return {
            "top_suppliers": top_5,
            "suggested_script": script
        }
