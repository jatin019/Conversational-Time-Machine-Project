from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from pathlib import Path

def load_vector_store(persona: str):
    persona = persona.lower().strip()

    if persona == "indira":
        path = Path("backend/data/faiss_indira")
    elif persona == "atal":
        path = Path("backend/data/faiss_atal")
    else:
        raise ValueError(f"Unknown persona '{persona}'. Expected 'atal' or 'indira'.")

    print(f"🧠 Loading vector store from: {path}")
    print(f"📂 Contents: {list(path.glob('*'))}")

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
