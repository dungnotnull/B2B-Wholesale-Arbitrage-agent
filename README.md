# B2B Wholesale Arbitrage Agent
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61dafb.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**The AI-powered commercial broker that finds factory-direct prices and negotiates deals for small shop owners.**

![Architecture](https://img.shields.io/badge/Architecture-Modular_Agentic-orange) ![Status](https://img.shields.io/badge/Status-Production_Ready-brightgreen)

---

## Overview

`B2B-Wholesale-Arbitrage-Agent` is a sophisticated AI system designed to eliminate the language and process barriers preventing small retailers from accessing the world's lowest wholesale prices (primarily via platforms like **1688.com**, **Taobao**, and **Alibaba**).

By combining **Computer Vision**, **Browser Automation**, and **Large Language Models (LLMs)**, the agent transforms a simple product image into a fully negotiated wholesale quote.

### Key Capabilities
- **Reverse Visual Sourcing**: Uses Google Vision API and CLIP to find the original factory source of any retail product.
- **AI Negotiation Broker**: A pluggable LLM chain (Claude -> GPT-4o -> Ollama) that acts as a senior procurement agent.
- **Cultural Nuance Engine**: Generates professional business scripts in Mandarin Chinese, tailored to specific negotiation personas.
- **Landed Cost Optimizer**: Calculates total costs including freight (Sea/Air/Express) and destination country duties.
- **Self-Improving Knowledge Base**: Automatically updates its research on e-commerce retrieval using crawl4ai.

---

## Architecture

```mermaid
graph TD
    A[User Image/URL] --> B[Vision Layer: Google Vision + CLIP]
    B --> C[Scraping Layer: Playwright Stealth]
    C --> D[Ranking Engine: Cosine Similarity]
    D --> E[LLM Broker: Claude/GPT/Ollama]
    E --> F[Negotiation: AliWangWang Automation]
    F --> G[Logistics Optimizer: Freightos/Customs]
    G --> H[User Dashboard: React UI]
```

### Tech Stack
- **Backend**: FastAPI, SQLAlchemy, Celery, Redis.
- **AI/ML**: PyTorch, Transformers (CLIP), Anthropic SDK, OpenAI SDK.
- **Automation**: Playwright (Stealth Mode).
- **Frontend**: React 18, Tailwind CSS, Axios.
- **Security**: AES-256-GCM Encryption for negotiation logs.

---

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- Ollama (Optional, for offline LLM)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/dungnotnull/B2B-Wholesale-Arbitrage-agent.git
   cd B2B-Wholesale-Arbitrage-agent
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r ../requirements.txt
   playwright install chromium
   cp .env.example .env # Fill in your API keys
   ```

3. **Frontend Setup**
   ```bash
   cd ../frontend
   npm install
   npm run dev
   ```

---

## API Reference

| Endpoint | Method | Description | Auth |
| :--- | :--- | :--- | :--- |
| `/api/v1/source` | `POST` | Find suppliers via image/URL | Required |
| `/api/v1/suppliers`| `GET` | Get ranked supplier list | Required |
| `/api/v1/negotiate`| `POST` | Start AI-driven negotiation | Required |
| `/health` | `GET` | System health check | Public |

---

## Security & Privacy
- **Encrypted Logs**: All supplier chat transcripts are stored using AES-256 encryption to protect commercial secrets.
- **Stealth Scraping**: Implements fingerprint randomization and request throttling to avoid platform blocks.

## License
Distributed under the MIT License. See LICENSE for more information.
