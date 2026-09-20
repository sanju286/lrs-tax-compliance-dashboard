# V2 Backend

## Run locally

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

API docs: http://127.0.0.1:8000/docs

V2 keeps storage in memory to make the demo easy to run. PostgreSQL is the next persistence step.

## Endpoints

- GET `/api/health`
- GET `/api/dashboard`
- GET `/api/remittances`
- POST `/api/remittances`
- GET `/api/transactions`
- POST `/api/transactions/import`
- GET `/api/compliance`
- GET `/api/tax-pack`
- POST `/api/assistant`
