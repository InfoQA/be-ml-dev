import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

models = {}

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")


def load_models():
    print("🔄 Loading embedding & FAISS index...")

    embedding_path = os.path.join(MODEL_DIR, "embedding_model")
    faiss_path = os.path.join(MODEL_DIR, "faiss_index3")

    if not os.path.exists(embedding_path):
        raise FileNotFoundError("Embedding model tidak ditemukan")

    if not os.path.exists(faiss_path):
        raise FileNotFoundError("FAISS index tidak ditemukan")

    # === Load Embedding ===
    embeddings = HuggingFaceEmbeddings(
        model_name=embedding_path
    )

    # === Load FAISS ===
    vector_db = FAISS.load_local(
        faiss_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    # Simpan ke global models
    models["vector_db"] = vector_db

    print("✅ Model berhasil dimuat:", list(models.keys()))
