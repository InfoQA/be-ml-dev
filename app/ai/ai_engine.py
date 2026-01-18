from app.ai.loader import models


def generate_answer(context: dict) -> str:
    retriever = models.get("retriever")
    if retriever is None:
        return "Sistem pencarian belum siap."

    question = context.get("question", "").strip()
    if not question:
        return "Silakan tuliskan pertanyaan Anda."

    try:
        docs = retriever.invoke(question)
    except Exception as e:
        print("Retrieval error:", e)
        return "Terjadi kesalahan saat mencari informasi."

    if not docs:
        return "Maaf, informasi yang Anda cari belum ditemukan."

    # 🔹 Ambil dokumen paling relevan
    answer = docs[0].page_content.strip()

    return (
        f"{answer}\n\n"
        "Ketik pertanyaan lain untuk topik ini,\n"
        "atau ketik 0 untuk kembali ke menu utama."
    )
