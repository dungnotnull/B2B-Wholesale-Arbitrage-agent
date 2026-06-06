# ADR 001: Choice of Architecture
- Decision: FastAPI Backend + React Frontend
- Rationale: Fast development, high performance for async I/O (Playwright/APIs), and a responsive dashboard for complex data comparison.

# ADR 002: Pluggable LLM Chain
- Decision: Abstract LLM class with Fallback Chain (Claude -> OpenAI -> Ollama)
- Rationale: Ensures high availability and cost control by falling back to local models if APIs fail or reach limits.

# ADR 003: SQLite for Local Storage
- Decision: SQLite with SQLAlchemy
- Rationale: Low overhead for early phases, easily migratable to PostgreSQL for production.
