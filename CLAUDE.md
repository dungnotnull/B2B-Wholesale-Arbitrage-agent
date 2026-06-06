# CLAUDE.md — b2b-wholesale-arbitrage

## Project Overview
- **Name**: b2b-wholesale-arbitrage
- **Tagline**: AI-powered wholesale sourcing agent that finds factory-direct prices and negotiates deals for small shop owners
- **Status**: Pre-development (Phase 0)
- **Current Phase**: Research & Environment Setup

---

## Core Problem Being Solved
Small shop owners and resellers on platforms like Shopee and Amazon struggle to find the original factory-direct source of products at the lowest wholesale prices. The main barriers are: (1) language barriers when dealing with Chinese/foreign suppliers on platforms like 1688, Taobao, and Alibaba; (2) complex negotiation processes around pricing, MOQ (Minimum Order Quantity), and shipping; (3) time-consuming manual reverse image searching and supplier comparison. This agent automates the entire sourcing pipeline — from a product image or retail link to a fully negotiated wholesale quote with logistics options — acting as a personal commercial broker powered by AI.

---

## Architecture Summary
- **Platform**: Python desktop app / web dashboard (FastAPI backend + React frontend)
- **Vision Stack**: Google Vision API / Azure Computer Vision for reverse image search; CLIP for local image embedding and similarity matching
- **NLP/LLM Stack**: Claude API (primary broker LLM), GPT-4 (fallback), local Ollama (Llama 3.1 for offline translation)
- **Scraping Layer**: Selenium + Playwright for headless browsing on 1688/Taobao/Alibaba
- **Negotiation Engine**: LLM-driven chat automation with business Chinese/English tone calibration
- **Logistics Optimizer**: Shipping rate aggregator (sea freight, air, express) with cost/time trade-off ranking
- **Local Storage**: SQLite for supplier database, product history, and negotiation logs

---

## Key Technical Decisions
1. Use **reverse image search** via Vision APIs to match retail product photos to wholesale listings across 1688/Taobao/Alibaba
2. LLM acts as a **commercial broker persona** — translates user intent into professional business Chinese/English negotiation scripts
3. **Playwright** for browser automation to interact with supplier chat systems (AliWangWang, TaoBao chat) and scrape pricing data
4. **Pluggable LLM backend**: Claude API → GPT-4 → local Ollama fallback chain, ensuring offline capability
5. **SQLite supplier registry**: Cache discovered suppliers, their MOQs, price tiers, and past negotiation outcomes locally
6. **Logistics aggregator**: Pull freight rates from multiple forwarders/APIs and rank by cost-per-kg vs. delivery time
7. All negotiation logs stored locally (AES-256 encrypted) for privacy and replay

---

## External LLM API Integrations

| Provider | Use Case | Config Key |
|----------|----------|------------|
| Claude API (claude-opus-4-8) | Primary negotiation broker, deal summarization | `CLAUDE_API_KEY` |
| OpenAI GPT-4o | Fallback negotiation, complex translation | `OPENAI_API_KEY` |
| Google Vision API | Reverse image search, product identification | `GOOGLE_VISION_API_KEY` |
| Azure Computer Vision | Fallback vision / OCR for Chinese product labels | `AZURE_VISION_KEY`, `AZURE_VISION_ENDPOINT` |
| DeepL / Google Translate | Fast bulk translation for product listings | `DEEPL_API_KEY` |

---

## HuggingFace Models in Use

| Model ID | Purpose | Link |
|----------|---------|------|
| `openai/clip-vit-large-patch14` | Local image embedding for similarity matching | [HF](https://huggingface.co/openai/clip-vit-large-patch14) |
| `Helsinki-NLP/opus-mt-zh-en` | Chinese → English translation (offline) | [HF](https://huggingface.co/Helsinki-NLP/opus-mt-zh-en) |
| `Helsinki-NLP/opus-mt-en-zh` | English → Chinese translation (offline) | [HF](https://huggingface.co/Helsinki-NLP/opus-mt-en-zh) |
| `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` | Multilingual product description matching | [HF](https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2) |

---

## Current Active Development Tasks
- [ ] Set up project structure and environment
- [ ] Integrate Google Vision API for reverse image search
- [ ] Build Playwright scraper for 1688 product search
- [ ] Implement CLIP-based local image similarity ranking
- [ ] Design LLM negotiation broker prompt templates
- [ ] Build supplier database schema (SQLite)
- [ ] Implement logistics rate aggregator
- [ ] Create FastAPI backend with React dashboard

---

## Related Files
- `PROJECT-detail.md` — Full technical specification and architecture
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` — Phase-by-phase development roadmap
- `SECOND-KNOWLEDGE-BRAIN.md` — Research papers, models, and self-updating knowledge base
