import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

models = {}

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")


def load_models():
    print("🔄 Loading models...")

    embedding_path = os.path.join(MODEL_DIR, "embedding_model")
    faiss_path = os.path.join(MODEL_DIR, "faiss_index")

    # === Embedding ===
    embeddings = HuggingFaceEmbeddings(
        model_name=embedding_path
    )

    # === FAISS ===
    vector_db = FAISS.load_local(
        faiss_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    models["retriever"] = vector_db.as_retriever(
        search_kwargs={"k": 3}
    )

    print("✅ Models loaded:", list(models.keys()))
