# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router
from app.vector_store import VectorStore
import os

app = FastAPI(title="AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.on_event("startup")
def startup_event():
    vector_db = VectorStore()
    if vector_db.is_empty():
        print("📥 Vector DB empty. Running ingestion...")
        os.system("python app/ingest.py")

@app.get("/")
def health():
    return {"status": "Backend running 🚀"}
