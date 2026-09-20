# ComplyInvest — LRS & Tax Compliance Dashboard V2

V2 adds a real FastAPI backend, REST API, CSV transaction import and an API-backed compliance assistant.

## Quick start

1. Open a terminal in `backend/`
2. Create/activate a Python virtual environment
3. `pip install -r requirements.txt`
4. `uvicorn main:app --reload`
5. Open `frontend/index.html`

API documentation: http://127.0.0.1:8000/docs

## Architecture

Browser UI -> FastAPI -> in-memory domain services

Next: PostgreSQL persistence -> versioned tax-rule engine -> Ollama explanation layer -> authentication -> document storage.

## Safety

All financial values are synthetic demo data. This is not tax or legal advice.
