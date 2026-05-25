import os
import uuid
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from main import run_crypto_crew
from memory.redis_memory import MemoryManager

load_dotenv("config/.env")

app = FastAPI(title="Crypto Research Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

memory = MemoryManager()

class QueryRequest(BaseModel):
    query: str
    session_id: str = "default"

class AlertRequest(BaseModel):
    coin: str
    threshold: float
    direction: str

@app.get("/")
def root():
    return {"status": "Crypto Agent API is running"}

@app.get("/health")
def health():
    return {"status": "ok", "agents": ["researcher", "analyst", "notifier"]}

@app.post("/query")
def query(req: QueryRequest):
    try:
        result = run_crypto_crew(req.query, req.session_id)
        return {
            "status": "success",
            "query": req.query,
            "result": str(result),
            "session_id": req.session_id
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/history/{session_id}")
def get_history(session_id: str):
    history = memory.get_session(session_id)
    return {"session_id": session_id, "history": history}

@app.get("/alerts")
def get_alerts():
    try:
        with open("alerts.log", "r") as f:
            alerts = f.readlines()
        return {"alerts": [a.strip() for a in alerts]}
    except FileNotFoundError:
        return {"alerts": []}

@app.delete("/history/{session_id}")
def clear_history(session_id: str):
    memory.r.delete(f"session:{session_id}")
    return {"status": "cleared", "session_id": session_id}
