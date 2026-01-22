from app.ai.loader import models


STOPWORDS = {
    "apa", "bagaimana", "kenapa", "jelaskan", "adalah",
    "program", "studi", "teknik", "informatika",
    "yang", "dan", "di", "ke", "dari", "untuk"
}


def generate_answer(context: dict) -> str:
    vector_db = models.get("vector_db")

    if vector_db is None:
        return "Sistem pencarian belum siap."

    question = context.get("question", "").strip()
    if not question:
        return "Silakan tuliskan pertanyaan Anda."

    # =========================
    # 1. BROAD SEARCH (FAISS)
    # =========================
    try:
        docs = vector_db.similarity_search(question, k=30)
    except Exception as e:
        print("❌ FAISS error:", e)
        return "Terjadi kesalahan saat mencari informasi."

    if not docs:
        return (
            "Maaf, informasi tidak ditemukan dalam "
            "panduan Program Studi Teknik Informatika Maranatha."
        )

    # =========================
    # 2. KEYWORD EXTRACTION
    # =========================
    keywords = [
        w.lower()
        for w in question.split()
        if w.lower() not in STOPWORDS
    ]

    # =========================
    # 3. RE-RANKING
    # =========================
    scored_docs = []

    for doc in docs:
        score = 0
        text_lower = doc.page_content.lower()

        for kw in keywords:
            if kw in text_lower:
                score += 1

        scored_docs.append({
            "doc": doc,
            "score": score
        })

    scored_docs.sort(key=lambda x: x["score"], reverse=True)

    best_match = scored_docs[0]

    # =========================
    # 4. OUT OF CONTEXT CHECK
    # =========================
    if best_match["score"] == 0:
        return (
            "Maaf, pertanyaan tersebut berada di luar konteks "
            "panduan Program Studi Teknik Informatika Maranatha.\n\n"
            "Silakan ketik 0 untuk kembali ke menu utama."
        )

    # =========================
    # 5. WINDOWING (500 CHAR)
    # =========================
    isi_teks = best_match["doc"].page_content
    isi_lower = isi_teks.lower()

    start_idx = 0
    if keywords:
        idx = isi_lower.find(keywords[0])
        if idx != -1:
            start_idx = idx

    line_start = isi_lower.rfind("\n", 0, start_idx)
    start_display = line_start + 1 if line_start != -1 else 0

    final_answer = isi_teks[start_display:start_display + 500]

    return (
        f"{final_answer}\n\n"
        "Ketik pertanyaan lain untuk topik ini,\n"
        "atau ketik 0 untuk kembali ke menu utama."
    )
