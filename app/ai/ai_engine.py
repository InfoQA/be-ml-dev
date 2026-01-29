import os
import re
from typing import Dict, List
from google import genai
from google.genai import types
from app.ai.loader import models

# =====================================================
# LOAD & VALIDATE API KEY
# =====================================================
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY belum ter-load.")

client = genai.Client(api_key=GOOGLE_API_KEY, http_options={'api_version': 'v1alpha'})
GEMINI_MODEL = "gemini-flash-latest"

# =====================================================
# STOPWORDS
# =====================================================
STOPWORDS = {
    "apa", "apakah", "bagaimana", "kenapa", "jelaskan", "adalah",
    "program", "studi", "teknik", "informatika",
    "yang", "dan", "di", "ke", "dari", "untuk"
}

# =====================================================
# TEXT UTILITIES
# =====================================================
def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_keywords(question: str) -> List[str]:
    tokens = question.split()
    keywords = [t for t in tokens if t not in STOPWORDS]
    return keywords if keywords else tokens[:2]

# =====================================================
# MAIN RAG PIPELINE
# =====================================================
def generate_answer(context: Dict) -> str:
    vector_db = models.get("vector_db")

    if vector_db is None:
        return "Sistem pencarian belum siap."

    raw_question = context.get("question", "").strip()
    if not raw_question:
        return "Silakan tuliskan pertanyaan Anda."

    normalized_question = normalize_text(raw_question)

    try:
        docs = vector_db.similarity_search(normalized_question, k=30)
    except Exception as e:
        print("FAISS error:", e)
        return "Terjadi kesalahan saat mencari informasi."

    if not docs:
        return (
            "Maaf, informasi tidak ditemukan dalam "
            "panduan Program Studi Teknik Informatika Maranatha."
        )

    keywords = extract_keywords(normalized_question)
    scored_docs = []

    for doc in docs:
        content = normalize_text(doc.page_content)
        score = sum(1 for kw in keywords if kw in content)

        scored_docs.append({
            "doc": doc,
            "score": score
        })

    scored_docs.sort(key=lambda x: x["score"], reverse=True)
    best_match = scored_docs[0]

    if best_match["score"] == 0:
        return (
            "Maaf, pertanyaan tersebut berada di luar konteks "
            "panduan Program Studi Teknik Informatika Maranatha.\n\n"
            "Silakan ketik 0 untuk kembali ke menu utama."
        )

    context_text = best_match["doc"].page_content[:1200]

    answer = generate_llm_answer(
        context_text=context_text,
        question=raw_question
    )

    return (
        f"{answer}\n\n"
        "Ketik pertanyaan lain untuk topik ini,\n"
        "atau ketik 0 untuk kembali ke menu utama."
    )


# =====================================================
# GEMINI GENERATION
# =====================================================
def generate_llm_answer(context_text: str, question: str) -> str:

    prompt = f"""
Anda adalah InfoQA yang merupakan sistem asisten akademik Program Studi Teknik Informatika bernama InfoQA.

Gunakan konteks berikut untuk menjawab pertanyaan pengguna
dengan bahasa Indonesia yang formal, jelas, dan manusiawi.
Jangan menyalin teks secara langsung.
Jangan menambahkan informasi di luar konteks.
Jangan ada sapaan Selamat pagi/siang/sore.
Langsung jawabannya saja.

KONTEKS:
{context_text}

PERTANYAAN:
{question}

JAWABAN:
"""

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        return response.text.strip()

    except Exception as e:
        print("Gemini error:", e)
        return "Terjadi kesalahan saat menghasilkan jawaban."