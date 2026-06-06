from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import anthropic
import openai
import requests
from backend.config import settings

@dataclass
class NegotiationContext:
    product_id: str
    user_intent: str
    target_price: float
    quantity: int
    history: List[Dict[str, Any]]
    language_target: str = "zh"

class LLMBackend(ABC):
    @abstractmethod
    async def generate(self, context: NegotiationContext) -> str:
        pass

    @abstractmethod
    async def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        pass

class ClaudeBackend(LLMBackend):
    def __init__(self, api_key: str):
        self.client = anthropic.AsyncAnthropic(api_key=api_key)

    async def generate(self, context: NegotiationContext) -> str:
        prompt = f"Act as a professional B2B sourcing broker. Goal: {context.user_intent}. Target Price: {context.target_price}. Quantity: {context.quantity}. History: {context.history}. Generate a professional business inquiry in {context.language_target}."
        
        message = await self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            system="You are an expert China procurement agent with 10 years experience in wholesale arbitrage.",
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text

    async def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        prompt = f"Translate the following from {source_lang} to {target_lang} while maintaining professional business tone: {text}"
        message = await self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text

class OpenAIBackend(LLMBackend):
    def __init__(self, api_key: str):
        self.client = openai.AsyncOpenAI(api_key=api_key)

    async def generate(self, context: NegotiationContext) -> str:
        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert China procurement agent."},
                {"role": "user", "content": f"Target Price: {context.target_price}, Quantity: {context.quantity}. Generate professional inquiry in {context.language_target}."}
            ]
        )
        return response.choices[0].message.content

    async def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": f"Translate {text} from {source_lang} to {target_lang}"}]
        )
        return response.choices[0].message.content

class OllamaBackend(LLMBackend):
    def __init__(self, model_id: str):
        self.model_id = model_id
        self.url = "http://localhost:11434/api/generate"

    async def generate(self, context: NegotiationContext) -> str:
        payload = {
            "model": self.model_id,
            "prompt": f"Professional B2B inquiry for product {context.product_id} in {context.language_target}",
            "stream": False
        }
        resp = requests.post(self.url, json=payload)
        return resp.json().get("response", "")

    async def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        payload = {
            "model": self.model_id,
            "prompt": f"Translate {text} from {source_lang} to {target_lang}",
            "stream": False
        }
        resp = requests.post(self.url, json=payload)
        return resp.json().get("response", "")

class LLMBroker:
    def __init__(self, backends: List[LLMBackend]):
        self.backends = backends

    async def negotiate(self, context: NegotiationContext) -> str:
        for backend in self.backends:
            try:
                return await backend.generate(context)
            except Exception as e:
                print(f"Backend {backend.__class__.__name__} failed: {e}")
                continue
        raise Exception("All LLM backends failed.")
