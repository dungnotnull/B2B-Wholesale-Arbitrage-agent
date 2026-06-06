from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import asyncio
from playwright.async_api import async_playwright, Page
from google.cloud import vision
from PIL import Image
import torch
from transformers import CLIPModel, CLIPProcessor

class VisionProvider(ABC):
    @abstractmethod
    async def reverse_image_search(self, image_path: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def get_image_embedding(self, image_path: str) -> List[float]:
        pass

class GoogleVisionProvider(VisionProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def reverse_image_search(self, image_path: str) -> List[Dict[str, Any]]:
        # Real implementation using Google Cloud Vision Web Detection
        client = vision.ImageAnnotatorClient()
        with open(image_path, "rb") as image_file:
            content = image_file.read()
        
        image = vision.Image(content=content)
        response = client.web_detection(image=image)
        
        results = []
        for page in response.web_detection.pages_with_matching_images:
            results.append({
                "url": page.url,
                "score": 1.0, # Google doesnt provide a precise similarity score for web pages
                "source": "google_vision"
            })
        return results

    async def get_image_embedding(self, image_path: str) -> List[float]:
        # Google Vision doesn't provide generic embeddings like CLIP
        raise NotImplementedError("Use LocalCLIPProvider for embeddings")

class LocalCLIPProvider(VisionProvider):
    def __init__(self, model_id: str):
        self.model_id = model_id
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = CLIPModel.from_pretrained(model_id).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(model_id)

    async def reverse_image_search(self, image_path: str) -> List[Dict[str, Any]]:
        return [] # CLIP is for similarity, not web search

    async def get_image_embedding(self, image_path: str) -> List[float]:
        image = Image.open(image_path)
        inputs = self.processor(images=image, return_tensors="pt").to(self.device)
        with torch.no_grad():
            image_features = self.model.get_image_features(**inputs)
        # Normalize and convert to list
        embedding = image_features / image_features.norm(p=2, dim=-1, keepdim=True)
        return embedding.cpu().tolist()[0]

class ScraperProvider(ABC):
    @abstractmethod
    async def extract_product_data(self, url: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def send_message(self, supplier_id: str, message: str) -> bool:
        pass

class PlaywrightScraper(ScraperProvider):
    def __init__(self):
        self.stealth_config = {
            "viewport": {"width": 1280, "height": 720},
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    async def extract_product_data(self, url: str) -> Dict[str, Any]:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(**self.stealth_config)
            page = await context.new_page()
            
            try:
                await page.goto(url, wait_until="domcontentloaded")
                # Target 1688 specific selectors
                title = await page.inner_text(".product-title") if await page.query_selector(".product-title") else "Unknown"
                price = await page.inner_text(".price-money") if await page.query_selector(".price-money") else "0"
                moq = await page.inner_text(".moq-value") if await page.query_selector(".moq-value") else "1"
                rating = await page.inner_text(".rating-score") if await page.query_selector(".rating-score") else "0"
                
                # Extract high-res image
                img_element = await page.query_selector("img.main-image")
                img_url = await img_element.get_attribute("src") if img_element else None
                
                return {
                    "title": title.strip(),
                    "price": float(price.replace("¥", "").strip()) if price != "0" else 0.0,
                    "moq": int(moq.strip()) if moq != "1" else 1,
                    "rating": float(rating.strip()) if rating != "0" else 0.0,
                    "image_url": img_url
                }
            except Exception as e:
                print(f"Scraper error: {e}")
                return {"error": str(e)}
            finally:
                await browser.close()

    async def send_message(self, supplier_id: str, message: str) -> bool:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False) # Real run needs visible or session-loaded browser
            context = await browser.new_context(**self.stealth_config)
            page = await context.new_page()
            
            try:
                # Navigation to AliWangWang / 1688 Chat
                await page.goto(f"https://1688.com/chat?supplier_id={supplier_id}")
                await page.wait_for_selector("[id="chat-input"]", timeout=10000)
                await page.fill("[id="chat-input"]", message)
                await page.press("[id="chat-input"]", "Enter")
                return True
            except Exception as e:
                print(f"Chat error: {e}")
                return False
            finally:
                await browser.close()
