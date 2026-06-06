# PROJECT-DEVELOPMENT-PHASE-TRACKING.md — b2b-wholesale-arbitrage

## Overview
16-week development roadmap from environment setup to production deployment.
Each phase has clear tasks, deliverables, success criteria, and effort estimates.

---

## Phase 0: Research & Environment Setup
**Timeline**: Week 1–2
**Goal**: Validate technical feasibility, set up toolchain, establish baseline scrapers

### Tasks
- [x] Study 1688.com and Alibaba.com DOM structure for scraping targets (product listing, price, MOQ, chat)
- [x] Test Google Vision API reverse image search accuracy on 10 sample products
- [x] Evaluate CLIP (ViT-L/14) for local image similarity ranking — measure accuracy vs. Google Vision
- [x] Research AliWangWang chat API / browser automation feasibility
- [x] Set up Python virtual environment, install all dependencies
- [x] Configure Docker Compose (FastAPI, Redis, SQLite)
- [x] Register API keys: Google Vision, Claude, OpenAI, DeepL
- [x] Prototype Playwright session on 1688 — manual login, basic search
- [x] Design SQLite schema: suppliers, products, negotiations, messages
- [x] Review legal/ToS considerations for web scraping 1688 and Alibaba

### Deliverables
- Working Playwright session that can load 1688 search results
- Google Vision API returning 5+ matching wholesale URLs for 3 test products
- SQLite schema finalized and migrated
- Docker Compose environment running

### Success Criteria
- Google Vision API finds correct product source on 1688 for ≥7/10 test products
- Playwright can navigate 1688 product search without CAPTCHA block (using stealth mode)
- All API keys validated and returning responses

### Estimated Effort: 2 engineers × 2 weeks = 4 person-weeks

---

## Phase 1: MVP — Core Sourcing Loop Working
**Timeline**: Week 3–6
**Goal**: End-to-end pipeline from product image → supplier list with prices

### Tasks
- [x] Build input handler: accept image upload OR URL, extract primary product image
- [x] Implement Google Vision API reverse search → extract top 10 wholesale platform URLs
- [x] Build 1688 product listing scraper (Playwright): title, price, MOQ, supplier rating, image URL
- [x] Implement CLIP image embedding pipeline: embed query image + scraped product images, compute cosine similarity
- [x] Build re-ranking logic: combine CLIP similarity score × supplier rating × price
- [x] Build supplier profile extractor: scrape supplier page (name, location, years active, transaction count)
- [x] Design negotiation context schema (product details, user requirements, target price, quantity)
- [x] Implement Claude API negotiation script generator (business Chinese inquiry template)
- [x] Build FastAPI endpoints: `/search`, `/suppliers`, `/negotiate`
- [x] Create minimal React dashboard: input form, supplier results table
- [x] Write unit tests for scraper, image pipeline, LLM client

### Deliverables
- Working `/search` endpoint: input image → returns top 5 ranked suppliers with price + MOQ
- LLM generates readable business Chinese inquiry script
- Basic React UI displaying results

### Success Criteria
- Pipeline completes full search in <2 minutes for a single product
- CLIP re-ranking improves top-1 accuracy by ≥15% over Vision API alone
- Generated Chinese negotiation script rated "professional" by native speaker evaluator
- Unit test coverage ≥70%

### Estimated Effort: 2 engineers × 4 weeks = 8 person-weeks

---

## Phase 2: ML/AI Integration — Smart Negotiation & Supplier Scoring
**Timeline**: Week 7–10
**Goal**: Add automated negotiation sending, response parsing, and supplier scoring

### Tasks
- [x] Implement Playwright automation to send inquiry message via AliWangWang chat interface
- [x] Build response poller: check chat inbox every 5–30 minutes for replies
- [x] Implement opus-mt (zh→en) translation pipeline for parsing supplier responses
- [x] Build LLM response parser: extract structured fields (quoted price, MOQ, lead time, shipping cost, payment terms)
- [x] Implement multi-round negotiation state machine (round 1: inquiry → round 2: counter-offer → round 3: accept/reject)
- [x] Build supplier scoring model: composite score from response rate, price delta, lead time, rating
- [x] Integrate DeepL API for high-quality translation fallback
- [x] Add Alibaba.com scraper as secondary source (English interface available)
- [x] Implement local BERT-based negotiation tone classifier (fine-tune on synthetic dialogue data)
- [x] Add Celery task queue for async processing (scraping + negotiation run in background)

### Deliverables
- Auto-send inquiry to top 3 suppliers, poll for responses, parse and display results
- Supplier scoring dashboard with sortable metrics
- Multi-round negotiation log with full transcript

### Success Criteria
- System successfully sends inquiry and receives response from ≥2/3 targeted suppliers within 24 hours
- Response parser extracts price/MOQ/lead time with ≥85% accuracy
- Multi-round negotiation achieves ≥10% price reduction vs. initial quote in test scenarios
- Celery queue handles 10 concurrent product searches without degradation

### Estimated Effort: 2 engineers × 4 weeks = 8 person-weeks

---

## Phase 3: External LLM API Integration — Full Broker Intelligence
**Timeline**: Week 11–12
**Goal**: Plug in full LLM broker chain with fallbacks; add logistics optimizer

### Tasks
- [x] Implement pluggable LLM backend class: Claude → GPT-4o → Ollama fallback chain
- [x] Fine-tune Claude system prompt for 5 negotiation personas (aggressive, friendly, formal, urgent, bulk-buyer)
- [x] Integrate Freightos API for sea/air freight rate quotes
- [x] Integrate 17Track API for shipment tracking
- [x] Build logistics optimizer: given supplier location + user warehouse → compute sea/air/express landed cost
- [x] Add duty/tariff estimator (HS code lookup + rate table for top 10 destination countries)
- [x] Implement Claude-powered deal summarization: executive summary of best supplier + recommended action
- [x] Add Ollama + Llama 3.1 8B for fully offline operation (no API keys required mode)
- [x] Build configuration panel in React: toggle LLM backend, set API keys, configure target country

### Deliverables
- Complete LLM fallback chain tested (all 3 backends producing valid output)
- Logistics comparison table in UI (sea vs. air vs. express, with landed cost)
- Full offline mode working with Ollama

### Success Criteria
- LLM chain gracefully falls back when primary API is unavailable (tested via mock failure injection)
- Logistics cost estimates within ±15% of real freight quotes (validated against 5 sample shipments)
- Offline mode produces valid negotiation scripts without internet access

### Estimated Effort: 2 engineers × 2 weeks = 4 person-weeks

---

## Phase 4: Self-Improving Knowledge Loop — SECOND-KNOWLEDGE-BRAIN Auto-Update
**Timeline**: Week 13–14
**Goal**: Automate supplier database enrichment and knowledge base updates

### Tasks
- [x] Build crawl4ai-based crawler targeting: Alibaba supplier profiles, 1688 seller ratings, trade news
- [x] Implement supplier re-verification scheduler: monthly re-check of cached suppliers (still active? updated pricing?)
- [x] Build price trend tracker: store historical price snapshots, compute rolling averages, alert on drops
- [x] Implement SECOND-KNOWLEDGE-BRAIN.md auto-updater: weekly crawl of ArXiv (cs.CV, cs.IR), HuggingFace Papers for new vision/NLP models relevant to product search
- [x] Add supplier community rating ingestion: scrape public review sources, aggregate into trust score
- [x] Build notification system: email/Telegram alerts for price drops, supplier re-ratings, new models found
- [x] Implement cache invalidation: auto-expire supplier data older than 30 days

### Deliverables
- Automated weekly KB update running via Celery Beat scheduler
- Price alert system sending Telegram notifications
- Supplier database self-refreshing without manual intervention

### Success Criteria
- KB auto-updater runs without errors for 2 consecutive weeks
- Price alerts fire within 1 hour of a tracked product dropping below threshold
- Supplier data freshness: ≥80% of cached suppliers have been verified within 30 days

### Estimated Effort: 2 engineers × 2 weeks = 4 person-weeks

---

## Phase 5: Testing, Polish & Deployment
**Timeline**: Week 15–16
**Goal**: Production-ready, documented, and deployable

### Tasks
- [ ] End-to-end integration test suite: 20 real products through full pipeline
- [ ] Performance optimization: target <90s for full search + negotiation script generation
- [ ] Security audit: review API key storage, SQLite encryption, Playwright session isolation
- [ ] CAPTCHA resilience: implement fingerprint randomization, request throttling, proxy rotation support
- [ ] UI polish: loading states, error messages, mobile-responsive layout
- [ ] Write user documentation: setup guide, API key configuration, first-search walkthrough
- [ ] Docker image build and push to Docker Hub / GHCR
- [ ] Deploy demo to Railway / Render with environment variable configuration
- [ ] Load test: 50 concurrent users, verify Celery queue handles backlog
- [ ] Create onboarding wizard: guided first-time setup (API keys → test search → first negotiation)

### Deliverables
- Production Docker image (multi-arch: amd64 + arm64)
- Complete test suite with ≥80% coverage
- Public deployment URL with demo mode
- User setup documentation

### Success Criteria
- E2E test pass rate ≥95% across 20 test products
- Full pipeline latency ≤90 seconds (p95)
- Zero critical security vulnerabilities in security audit
- User setup time ≤15 minutes from fresh clone to first successful search

### Estimated Effort: 2 engineers × 2 weeks = 4 person-weeks

---

## Total Estimated Effort
| Phase | Duration | Person-Weeks |
|-------|----------|-------------|
| Phase 0: Research & Setup | Week 1–2 | 4 |
| Phase 1: MVP Core Loop | Week 3–6 | 8 |
| Phase 2: ML/AI Integration | Week 7–10 | 8 |
| Phase 3: LLM API Integration | Week 11–12 | 4 |
| Phase 4: Self-Improving KB | Week 13–14 | 4 |
| Phase 5: Testing & Deployment | Week 15–16 | 4 |
| **Total** | **16 weeks** | **32 person-weeks** |

---

## Key Risks & Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| 1688/Taobao blocks Playwright scraper | High | High | Stealth mode, proxy rotation, request rate limiting, human-like delays |
| Google Vision API cost overrun | Medium | Medium | Cache all image embeddings locally with CLIP; use Vision API only for new images |
| AliWangWang chat automation blocked | High | Medium | Fall back to email/contact form outreach; manual copy-paste mode |
| LLM-generated Chinese rejected as bot | Medium | Medium | Human review mode: LLM drafts, user approves before sending |
| Logistics API data inaccurate | Medium | Low | Show estimates with ±20% disclaimer; link to manual rate check |



