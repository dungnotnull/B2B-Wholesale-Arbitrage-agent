from typing import Dict, Any
import requests

class LogisticsOptimizer:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def calculate_landed_cost(self, supplier_loc: str, dest_loc: str, weight_kg: float, volume_m3: float) -> Dict[str, Any]:
        # Real Integration with Freightos API
        url = "https://api.freightos.com/v3/quotes"
        payload = {
            "origin": supplier_loc,
            "destination": dest_loc,
            "weight": weight_kg,
            "volume": volume_m3
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=10)
            return resp.json()
        except Exception as e:
            return {"error": f"Freightos API failed: {e}"}

    def estimate_duties(self, hs_code: str, destination_country: str) -> float:
        # Real implementation: use a lookup table or a 3rd party customs API
        duty_table = {"US": {"electronics": 0.05, "textiles": 0.12}, "VN": {"electronics": 0.02}}
        return duty_table.get(destination_country, {}).get("electronics", 0.10)

class PersonaManager:
    PERSONAS = {
        "aggressive": "You are a ruthless procurement agent. Leverage volume to force price drops. Be firm and direct.",
        "friendly": "You are building a long-term partnership. Use polite, respectful business Chinese (guanxi).",
        "formal": "You are a corporate agent. Focus on specifications, certifications, and ISO standards.",
        "urgent": "You are a fast-moving retailer. prioritize delivery speed and sample availability over long-term terms."
    }

    def get_system_prompt(self, strategy: str) -> str:
        return self.PERSONAS.get(strategy, self.PERSONAS["formal"])
