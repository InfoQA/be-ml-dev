from app.ai.loader import models


def build_retrieval_query(context: dict) -> str:

    query_parts = []

    if context.get("menu"):
        query_parts.append(context["menu"].replace("_", " "))

    if context.get("sub_menu"):
        query_parts.append(context["sub_menu"].replace("_", " "))

    if context.get("semester"):
        query_parts.append(f"semester {context['semester']}")

    if context.get("question"):
        query_parts.append(context["question"])

    return " ".join(query_parts).strip()


def generate_answer(context: dict) -> str:
    retriever = models.get("retriever")

    if retriever is None:
        return "Sistem pencarian belum siap."

    query = build_retrieval_query(context)

    try:
        docs = retriever.invoke(query)
    except Exception as e:
        return "Terjadi kesalahan saat mencari informasi."

    if not docs:
        return "Maaf, informasi yang Anda cari belum ditemukan."

    # Ambil jawaban terbaik dari FAISS
    return docs[0].page_content
