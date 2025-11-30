from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict

app = FastAPI()

# Supaya frontend React bisa mengakses API
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Format JSON yang diharuskan oleh API
class RequestBody(BaseModel):
    message: str

# 1. Kontrak request
class ChatRequest(BaseModel):
    message: str

# 2. Kontrak response
class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):

    generated_reply = f"Pesan diterima: {req.message}"

    return ChatResponse(reply=generated_reply)