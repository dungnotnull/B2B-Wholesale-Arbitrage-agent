from typing import List, Dict, Any, Optional
from backend.vision_scraper import ScraperProvider
from backend.llm_broker import LLMBackend, NegotiationContext
import json

class SmartNegotiator:
    def __init__(self, scraper: ScraperProvider, broker: LLMBackend):
        self.scraper = scraper
        self.broker = broker

    async def execute_negotiation_cycle(self, supplier_id: str, context: NegotiationContext):
        # 1. Generate and Send
        script = await self.broker.generate(context)
        success = await self.scraper.send_message(supplier_id, script)
        
        if not success:
            return {"status": "failed", "error": "Message sending failed"}

        # 2. Polling Logic (Simplified for current structure)
        # In real run, this would be a Celery task that polls every 30 mins
        response = await self._poll_for_response(supplier_id)
        
        # 3. LLM-based structured parsing
        parsed_data = await self._parse_supplier_offer(response, context)
        
        # 4. Composite Scoring
        score = self._calculate_supplier_score(parsed_data, context.target_price)
        
        return {
            "offer": parsed_data,
            "score": score,
            "status": "responded"
        }

    async def _poll_for_response(self, supplier_id: str) -> str:
        # REAL logic: use playwright to check chat history for new messages from supplier_id
        # For this "ready-for-run" code, we provide the logic flow
        return "We can offer $ la price of 8.0 USD per unit for 500pcs. Lead time 10 days."

    async def _parse_supplier_offer(self, text: str, context: NegotiationContext) -> Dict[str, Any]:
        # The "Real" way: ask the LLM to return a JSON schema
        prompt = f"Extract the following fields in JSON: quoted_price, moq, lead_time, shipping_cost. Text: {text}"
        parsed_text = await self.broker.generate(context) # In reality, use a specific translation/parsing method
        try:
            return json.loads(parsed_text)
        except:
            # Fallback logic if LLM doesn't return perfect JSON
            return {"quoted_price": 0.0, "error": "Parsing failed"}

    def _calculate_supplier_score(self, offer: Dict[str, Any], target: float) -> float:
        price = offer.get("quoted_price", 9999)
        if price == 0: return 0.0
        # Score based on proximity to target price (0 to 100)
        price_score = max(0, 100 * (1 - abs(target - price) / target))
        return price_score
