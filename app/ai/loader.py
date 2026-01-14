import os
from transformers import pipeline
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

models = {}

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")


def load_models():
    print("🔄 Loading models...")

    # ===== PATH =====
    embedding_path = os.path.join(MODEL_DIR, "embedding_model")
    faiss_path = os.path.join(MODEL_DIR, "faiss_index")
    chatbot_path = os.path.join(MODEL_DIR, "chatbot_model")

    # ===== 1. EMBEDDING MODEL =====
    embeddings = HuggingFaceEmbeddings(
        model_name=embedding_path
    )

    # ===== 2. FAISS VECTOR STORE =====
    vector_db = FAISS.load_local(
        faiss_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    models["retriever"] = vector_db.as_retriever(
        search_kwargs={"k": 3}
    )

    # ===== 3. INTENT / CHAT MODEL =====
    if not os.path.exists(chatbot_path):
        raise RuntimeError("Folder chatbot_model tidak ditemukan")

    models["chat_model"] = pipeline(
        "text-generation",
        model=chatbot_path,
        tokenizer=chatbot_path,
        max_new_tokens=256,
        do_sample=True,
        temperature=0.7,
    )

    print("Models loaded:", list(models.keys()))
