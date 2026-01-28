from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.core.state import reset_conversation, handle_message
from app.ai.loader import load_models

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:4173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# SCHEMA
# =========================
class ChatRequest(BaseModel):
    message: str


class ChatData(BaseModel):
    message: str
    reply: str

class ChatResponse(BaseModel):
    message: str
    data: ChatData

@app.on_event("startup")
def startup_event():
    load_models()

# =========================
# ENDPOINT
# =========================
@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    user_message = req.message.strip()

    if user_message == "__init__":
        reset_conversation()
        reply = (
            "Halo, selamat datang di Chatbot Panduan Teknik Informatika.\n"
            "Silakan pilih menu berikut:\n"
            "1. Mata Kuliah\n"
            "2. MBKM\n"
            "3. Informasi Umum"
        )
    else:
        reply = handle_message(user_message)

    return ChatResponse(
        message="message telah berhasil dikirim",
        data=ChatData(
            message=user_message,
            reply=reply
        )
    )