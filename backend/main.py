from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import io


app = FastAPI(title="LRS & Tax Compliance API", version="2.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LRS_LIMIT_USD = 250000.0

REM = [
    {"date":"2026-09-12","inr":200000,"usd":2300,"purpose":"US equities","status":"Completed"},
    {"date":"2026-08-28","inr":150000,"usd":1720,"purpose":"US equities","status":"Completed"},
    {"date":"2026-08-10","inr":300000,"usd":3420,"purpose":"US equities","status":"Completed"},
    {"date":"2026-07-15","inr":250000,"usd":2850,"purpose":"US equities","status":"Completed"},
    {"date":"2026-06-20","inr":120000,"usd":1390,"purpose":"US equities","status":"Completed"},
]

TX = [
    {"date":"2026-04-10","symbol":"AAPL","type":"BUY","quantity":5,"price_usd":170},
    {"date":"2026-05-02","symbol":"MSFT","type":"BUY","quantity":4,"price_usd":410},
    {"date":"2026-06-20","symbol":"AAPL","type":"SELL","quantity":2,"price_usd":195},
    {"date":"2026-07-15","symbol":"NVDA","type":"BUY","quantity":3,"price_usd":145},
    {"date":"2026-08-10","symbol":"MSFT","type":"SELL","quantity":1,"price_usd":455},
]

class Remittance(BaseModel):
    date: str
    inr: float
    usd: float
    purpose: str = "US equities"
    status: str = "Completed"

class Question(BaseModel):
    question: str

@app.get("/api/health")
def health():
    return {"status":"ok","version":"2.0.0"}

@app.get("/api/dashboard")
def dashboard():
    used = sum(x["usd"] for x in REM)
    return {
        "lrs_limit_usd": LRS_LIMIT_USD,
        "lrs_used_usd": used,
        "lrs_utilization_pct": round(used/LRS_LIMIT_USD*100,2),
        "lrs_remaining_usd": round(LRS_LIMIT_USD-used,2),
        "remittance_count": len(REM),
        "transaction_count": len(TX),
        "compliance_score": 78,
        "review_items": 2
    }

@app.get("/api/remittances")
def remittances():
    return REM

@app.post("/api/remittances")
def add_remittance(item: Remittance):
    REM.insert(0, item.model_dump())
    return {"message":"Remittance added","item":REM[0]}

@app.get("/api/transactions")
def transactions():
    return TX

@app.post("/api/transactions/import")
async def import_transactions(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(400, "Upload a CSV file")
    raw = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(raw))
    except Exception as e:
        raise HTTPException(400, f"Invalid CSV: {e}")
    required = {"date","symbol","type","quantity","price_usd"}
    missing = required - set(df.columns)
    if missing:
        raise HTTPException(400, f"Missing columns: {sorted(missing)}")
    records = df[list(required)].to_dict("records")
    TX.extend(records)
    return {"imported":len(records),"transactions":records}

@app.get("/api/compliance")
def compliance():
    return [
        {"name":"LRS transactions","status":"ready","message":"Tracked remittances are reconciled"},
        {"name":"Capital gains","status":"ready","message":"Buy/sell records are available"},
        {"name":"Foreign assets","status":"review","message":"One acquisition field needs review"},
        {"name":"Foreign tax credit","status":"review","message":"Supporting withholding statement required"},
    ]

@app.get("/api/tax-pack")
def tax_pack():
    return {
        "financial_year":"2026-27",
        "short_term_gains_inr":12500,
        "long_term_gains_inr":35750,
        "dividends_inr":35200,
        "foreign_tax_paid_inr":8750,
        "lrs_used_usd":sum(x["usd"] for x in REM),
        "compliance_score":78,
        "note":"Illustrative demo figures; verify current tax rules before use."
    }

@app.post("/api/assistant")
def assistant(q: Question):
    text=q.question.lower()
    if "lrs" in text:
        d=dashboard()
        return {"answer":f"Your demo workspace uses ${d['lrs_used_usd']:,.0f} of the ${LRS_LIMIT_USD:,.0f} configurable LRS limit ({d['lrs_utilization_pct']}%)."}
    if "tax" in text:
        return {"answer":"The demo tax pack contains ₹12,500 short-term gains, ₹35,750 long-term gains, ₹35,200 dividends and ₹8,750 foreign tax paid. These are illustrative figures."}
    return {"answer":"Start with the two review items: complete the missing acquisition information and attach the foreign-tax withholding statement. Then regenerate the tax working pack."}
