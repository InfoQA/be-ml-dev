from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# =========================
# CORS
# =========================
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

# =========================
# STATE GLOBAL (1 USER)
# =========================
conversation_state = "WAIT_MENU"
conversation_data = {}

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

# =========================
# ENDPOINT
# =========================
@app.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    global conversation_state, conversation_data

    user_message = req.message.strip()

    # -------------------------
    # INIT (PAGE LOAD / REFRESH)
    # -------------------------
    if user_message == "__init__":
        conversation_state = "WAIT_MENU"
        conversation_data.clear()

        return ChatResponse(
            message="message telah berhasil dikirim",
            data=ChatData(
                message=user_message,
                reply=(
                    "Halo, selamat datang di Chatbot Panduan Teknik Informatika.\n"
                    "Silakan pilih menu berikut:\n"
                    "1. Kurikulum dan Mata Kuliah\n"
                    "2. MBKM\n"
                    "3. Informasi Umum"
                )
            )
        )

    # -------------------------
    # TAHAP 3 - VALIDASI MENU
    # -------------------------
    if conversation_state == "WAIT_MENU":

        if user_message not in ["1", "2", "3"]:
            return ChatResponse(
                message="message telah berhasil dikirim",
                data=ChatData(
                    message=user_message,
                    reply="Pilihan tidak valid. Silakan masukkan angka 1, 2, atau 3."
                )
            )

        # SIMPAN PILIHAN MENU
        conversation_data["menu"] = user_message

        # PINDAH STATE
        conversation_state = "WAIT_QUESTION"

        # RESPON BERDASARKAN MENU
        if user_message == "1":
            reply_text = "Anda memilih Kurikulum dan Mata Kuliah.\nSilakan tuliskan pertanyaan Anda."
        elif user_message == "2":
            reply_text = "Anda memilih MBKM.\nSilakan tuliskan pertanyaan Anda."
        else:
            reply_text = "Anda memilih Informasi Umum.\nSilakan tuliskan pertanyaan Anda."

        return ChatResponse(
            message="message telah berhasil dikirim",
            data=ChatData(
                message=user_message,
                reply=reply_text
            )
        )

    # -------------------------
    # TAHAP SELANJUTNYA (DUMMY)
    # -------------------------
    if conversation_state == "WAIT_QUESTION":
        # SIMPAN PERTANYAAN USER
        conversation_data["question"] = user_message

        return ChatResponse(
            message="message telah berhasil dikirim",
            data=ChatData(
                message=user_message,
                reply=(
                    "Pertanyaan Anda telah diterima.\n"
                    "(Tahap berikutnya: akan dikirim ke model AI)"
                )
            )
        )

    # -------------------------
    # FALLBACK
    # -------------------------
    return ChatResponse(
        message="message telah berhasil dikirim",
        data=ChatData(
            message=user_message,
            reply="Terjadi kesalahan state. Silakan refresh halaman."
        )
    )
