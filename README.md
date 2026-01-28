# InfoQA Back-end API & Machine Learning

****
Backend service berbasis **FastAPI** yang mengimplementasikan
**Retrieval-Augmented Generation (RAG)** menggunakan **FAISS**,  
**HuggingFace Embeddings**, dan **Google Gemini** untuk menyediakan
asisten informasi akademik Program Studi Teknik Informatika.

---

## 📁 Struktur Direktori
```
be-ml-dev/
├── app/
│   ├── ai/
│   │   ├── ai_engine.py        # RAG + Gemini pipeline
│   │   └── loader.py           # Load embedding & FAISS index
│   ├── core/
│   │   └── state.py            # Finite State Conversation Handler
│   └── models/
│       ├── embedding_model/    # Model embedding
│       └── faiss_index/        # FAISS index
│
├── main.py                     # Entry point FastAPI
├── .env.example                # Template environment variable
├── .gitignore
├── README.md
├── venv/                       # Virtual environment (ignored)
└── venvvenv/                   # Virtual environment (ignored)
```

---

## ⚙️ Prasyarat
- Python **3.9+**
- pip
- Virtual environment (venv)
- Google Gemini API Key

---

## 🚀 Cara Menjalankan Aplikasi

### 1️⃣ Clone repository
```bash
  git clone <repository-url>
  cd be-ml-dev
```

---

### 2️⃣ Buat & aktifkan virtual environment
```bash
  python -m venv venv
```

**Windows**
```bash
  venv\Scripts\activate
```

**Linux / macOS**
```bash
  source venv/bin/activate
```

---

### 3️⃣ Install dependency
```bash
  pip install -r requirements.txt
```

> Jika `requirements.txt` belum tersedia:
```bash
  pip install fastapi uvicorn python-dotenv langchain faiss-cpu langchain-community langchain-huggingface google-generativeai
```

---

### 4️⃣ Setup environment variable
```bash
  cp .env.example .env
```

Isi `GOOGLE_API_KEY` pada file `.env`.

---

### 5️⃣ Jalankan server FastAPI
```bash
  uvicorn app.main:app --reload
```

Jika berhasil:
```
Uvicorn running on http://127.0.0.1:8000
```

---

## 🌐 Dokumentasi API

### Swagger UI
```
http://127.0.0.1:8000/docs
```
- Testing endpoint
- Digunakan saat development

### ReDoc
```
http://127.0.0.1:8000/redoc
```
- Dokumentasi API versi ringkas
- Read-only

---

## 🧠 Fitur Utama
- Finite State Conversation (menu → sub menu → pertanyaan)
- Retrieval menggunakan **FAISS similarity search**
- Generative Answer menggunakan **Google Gemini**
- Context-aware academic assistant

---

## 📌 Catatan
Project ini dikembangkan untuk kebutuhan:
- Akademik
- Riset
- Prototipe asisten informasi berbasis AI

Tidak ditujukan untuk deployment publik tanpa pengamanan tambahan.