# PROJECT-detail.md — b2b-wholesale-arbitrage

## Executive Summary
b2b-wholesale-arbitrage is an AI agent that eliminates the language and process barriers preventing small shop owners from accessing factory-direct wholesale prices. By combining computer vision (reverse image search), browser automation, and an LLM-powered negotiation broker, the system automates the full sourcing pipeline: from a product photo or retail URL to a ranked list of vetted suppliers with negotiated prices, MOQ terms, and optimized shipping options — all without the user speaking a word of Chinese.

---

## Problem Statement
The global cross-border wholesale market (Taobao, 1688, Alibaba) represents trillions of dollars in inventory accessible at 40–70% below retail prices. However, 95%+ of small shop owners in Southeast Asia and the West are locked out because:

- **Language barrier**: The best prices are on Chinese-only platforms (1688.com) where UI, listings, and supplier chat are in Mandarin
- **Negotiation complexity**: Securing factory prices requires understanding MOQ tiers, sample policies, payment terms, and shipping consolidation — knowledge most small sellers don't have
- **Time cost**: Manually searching, comparing, and communicating with 10–20 suppliers per product takes 3–8 hours
- **Platform opacity**: Retail listings (Shopee, Amazon) don't disclose sourcing origin, making reverse-sourcing non-trivial

**Market data**: The global B2B e-commerce market is projected to reach $36 trillion by 2026 (Statista 2023). Over 2 million active sellers on Shopee Southeast Asia report sourcing costs as their #1 operational pain point. 1688.com alone hosts 140+ million product listings with no English interface.

---

## Target Users & Use Cases

### Primary Users
- Small shop owners (1–10 employees) selling on Shopee, Lazada, Amazon, TikTok Shop
- Dropshippers and print-on-demand resellers
- Individual entrepreneurs doing product arbitrage

### Use Cases
1. **Product Sourcing**: Find the wholesale factory source for any product seen on a retail platform
2. **Price Benchmarking**: Compare prices across 5–10 suppliers for the same product
3. **Automated Negotiation**: Let the AI broker negotiate price, MOQ, samples, and payment terms on behalf of the user
4. **Logistics Planning**: Get ranked shipping options (sea freight vs. air vs. express) with cost and time estimates
5. **Supplier Vetting**: Score suppliers based on transaction history, ratings, and response patterns

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE LAYER                         │
│         FastAPI Backend + React Dashboard / Telegram Bot             │
└────────────────────────┬────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────────┐
│                       ORCHESTRATION LAYER                            │
│              Agent Manager (LangChain / custom loop)                 │
│   [Input Parser] → [Search Engine] → [Negotiator] → [Summarizer]    │
└──────┬─────────────────┬──────────────────┬─────────────────────────┘
       │                 │                  │
┌──────▼──────┐  ┌───────▼───────┐  ┌──────▼──────────────────────────┐
│ VISION      │  │ SCRAPING      │  │ LLM BROKER LAYER                 │
│ LAYER       │  │ LAYER         │  │                                  │
│             │  │               │  │ Claude API (primary)             │
│ Google      │  │ Playwright    │  │ GPT-4o (fallback)                │
│ Vision API  │  │ (1688/Taobao/ │  │ Ollama Llama3 (offline)          │
│             │  │  Alibaba)     │  │                                  │
│ CLIP        │  │               │  │ Negotiation Script Engine        │
│ (local)     │  │ Selenium      │  │ Translation Module               │
│             │  │ (chat bots)   │  │ (opus-mt zh↔en + DeepL)          │
└──────┬──────┘  └───────┬───────┘  └──────┬──────────────────────────┘
       │                 │                  │
┌──────▼─────────────────▼──────────────────▼─────────────────────────┐
│                         DATA LAYER                                    │
│   SQLite (suppliers, negotiations, products)   AES-256 encryption    │
│   Local cache: image embeddings, price history, shipping rates       │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Component | Technology | Source |
|-----------|-----------|--------|
| Backend API | FastAPI 0.111+ | PyPI |
| Frontend | React 18 + TailwindCSS | npm |
| Browser Automation | Playwright 1.44+ | PyPI / npm |
| Vision API | Google Cloud Vision API | GCP |
| Local Image Embedding | CLIP (openai/clip-vit-large-patch14) | HuggingFace |
| Primary LLM | Claude API (claude-opus-4-8) | Anthropic |
| Fallback LLM | GPT-4o | OpenAI |
| Offline LLM | Ollama + Llama 3.1 8B | ollama.ai |
| Translation (offline) | Helsinki-NLP opus-mt models | HuggingFace |
| Translation (online) | DeepL API | deepl.com |
| Database | SQLite + SQLAlchemy | PyPI |
| Encryption | cryptography (AES-256-GCM) | PyPI |
| Task Queue | Celery + Redis | PyPI |
| Logistics APIs | Freightos API, 17Track API | 3rd party |
| Containerization | Docker + Docker Compose | docker.com |

---

## ML/DL Models

### Vision Models
| Model ID | Purpose | Source |
|----------|---------|--------|
| `openai/clip-vit-large-patch14` | Image-to-embedding for similarity ranking | HuggingFace |
| Google Vision API | Reverse image search, web entity detection | GCP API |
| Azure Computer Vision 4.0 | OCR for Chinese product labels, image analysis | Azure API |

### NLP / Translation Models
| Model ID | Purpose | Source |
|----------|---------|--------|
| `Helsinki-NLP/opus-mt-zh-en` | Chinese → English offline translation | HuggingFace |
| `Helsinki-NLP/opus-mt-en-zh` | English → Chinese offline translation | HuggingFace |
| `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` | Cross-lingual product description matching | HuggingFace |

### Fine-Tuning Plan
- **Negotiation tone classifier**: Fine-tune a small BERT-based model on wholesale negotiation dialogues to classify supplier responsiveness (cooperative / evasive / high-risk). Training data: scraped 1688 chat transcripts + synthetic data generated by Claude.
- **Product category classifier**: Fine-tune on 1688/Alibaba product taxonomy for accurate category routing. Training data: 1688 public product listings.

---

## External LLM API Integration

### Pluggable Backend Design
```python
class LLMBroker:
    def __init__(self):
        self.chain = [
            ClaudeBackend(model="claude-opus-4-8"),
            OpenAIBackend(model="gpt-4o"),
            OllamaBackend(model="llama3.1:8b")
        ]
    
    async def negotiate(self, context: NegotiationContext) -> str:
        for backend in self.chain:
            try:
                return await backend.generate(context)
            except (RateLimitError, APIError):
                continue
        raise AllBackendsFailedError()
```

### Negotiation Broker System Prompt (Claude)
The LLM is instructed to act as a professional B2B sourcing broker:
- Persona: Senior procurement agent with 10+ years China trade experience
- Output: Professional business Chinese/English scripts tailored to supplier type (factory vs. trading company)
- Tasks: Price negotiation, MOQ reduction requests, sample requests, payment term discussion, shipping cost inquiry

---

## Feature Specification

### MVP Features
- [x] Input: product image upload OR retail URL (Shopee, Amazon, AliExpress)
- [x] Reverse image search via Google Vision API → find matching products on 1688/Alibaba
- [x] Playwright scraper: extract product listings, prices, supplier info from 1688
- [x] CLIP-based local re-ranking of results by visual similarity
- [x] LLM generates negotiation script in business Chinese
- [x] Auto-send inquiry message to top 3 suppliers (via browser automation)
- [x] Parse and translate supplier responses
- [x] Display ranked results: supplier name, price, MOQ, shipping estimate
- [x] Save supplier and negotiation data to local SQLite

### Advanced Features
- [ ] Automated multi-round negotiation (counter-offer, volume discount requests)
- [ ] Supplier scoring system (response rate, price competitiveness, delivery history)
- [ ] Logistics optimizer: compare sea/air/express with duty estimation
- [ ] Bulk sourcing mode: process 10+ products simultaneously
- [ ] Telegram bot interface for mobile sourcing on-the-go
- [ ] Price trend tracking: alert when supplier price drops below threshold
- [ ] Sample order automation: auto-place sample orders via Alipay integration
- [ ] Self-improving supplier database: agents re-verify suppliers monthly

---

## Full E2E Data Flow

1. **Input**: User uploads product image OR pastes retail URL (Shopee/Amazon)
2. **Image Extraction**: If URL, Playwright scrapes primary product image; if upload, use directly
3. **Reverse Vision Search**: Send image to Google Vision API → get web entities + visually similar pages on wholesale platforms
4. **Platform Scraping**: Playwright opens 1688/Alibaba → search by image/keyword → extract top 10–20 listings (title, price, MOQ, supplier rating, location)
5. **Local Re-ranking**: CLIP embeds query image + product images → cosine similarity score → re-rank by visual match
6. **Supplier Selection**: Filter top 5 suppliers by score × rating × price
7. **Negotiation Script Generation**: Claude API generates personalized inquiry in business Chinese, including: price for X units, MOQ flexibility, sample availability, shipping cost to user's country
8. **Auto-Send**: Playwright automates sending the script via supplier chat interface (AliWangWang)
9. **Response Polling**: Monitor chat for replies (polling interval: 5–30 min)
10. **Response Parsing**: LLM + opus-mt translates and extracts structured data (price offer, MOQ, lead time, shipping quote)
11. **Logistics Calculation**: Query Freightos/17Track APIs for freight rates; calculate total landed cost
12. **Summarization**: Claude generates executive summary: best deal, recommended supplier, logistics plan
13. **Output**: User dashboard shows ranked supplier comparison table + recommended action

---

## Privacy & Security
- All negotiation chat logs stored locally in AES-256-GCM encrypted SQLite
- API keys stored in `.env` file, never logged or transmitted
- Playwright sessions use isolated browser profiles (no credential sharing)
- Optional: route all scraping traffic through user-provided proxy/VPN
- No user data sent to third parties except: product images to Google Vision API (configurable to disable), LLM prompts to Claude/OpenAI (contains only product descriptions, no PII)
- GDPR-compliant: all data deletable via single command

---

## Key Python Dependencies

```
fastapi==0.111.0
uvicorn==0.29.0
playwright==1.44.0
selenium==4.21.0
anthropic==0.28.0
openai==1.30.0
transformers==4.41.0
torch==2.3.0
sentence-transformers==3.0.0
Pillow==10.3.0
sqlalchemy==2.0.30
cryptography==42.0.8
celery==5.4.0
redis==5.0.4
httpx==0.27.0
python-dotenv==1.0.1
pydantic==2.7.0
langchain==0.2.0
langchain-anthropic==0.1.15
```

---

## Improvement Suggestions

1. **AliExpress Integration**: Add AliExpress as a mid-tier sourcing option (English interface, lower MOQs) for users not ready for direct factory sourcing
2. **Competitor Price Monitor**: Continuously monitor competitor retail listings and alert when their margin exceeds a threshold, suggesting a resourcing opportunity
3. **Quality Verification Agent**: Integrate with third-party China inspection services (SGS, Bureau Veritas) — auto-request inspection quotes when order exceeds threshold value
4. **Payment Escrow Integration**: Connect with Alibaba Trade Assurance or PayPal for safe payment with built-in buyer protection
5. **Community Supplier Ratings**: Allow users to share (anonymized) supplier experiences to build a community-verified supplier quality score
6. **Tariff & Duty Calculator**: Auto-calculate import duties based on HS code, origin country, and destination — include in total cost comparison
7. **Factory Audit Score**: Scrape Alibaba supplier profile data (years active, verified status, production capacity, export experience) to build composite trust score
8. **Multi-language Support**: Extend negotiation to Korean (Gmarket), Japanese (Rakuten supplier side), and Vietnamese (Vietnamese wholesale platforms) beyond Chinese
9. **WhatsApp/WeChat Integration**: Many suppliers communicate via WhatsApp/WeChat — add bridge automation for these channels
10. **Return & Dispute Automation**: If quality issues arise post-delivery, auto-generate dispute messages and evidence packages in the supplier's language
