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

class ChatRequest(BaseModel):
    message: str

class ChatData(BaseModel):
    message: str
    reply : str

class ChatResponse(BaseModel):
    message : str
    data: ChatData

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    generated_reply = f"Pesan diterima: {req.message}"

    return ChatResponse(
        message="message telah berhasil dikirim",
        data=ChatData(
            message=req.message,
            reply=generated_reply
        )
    )