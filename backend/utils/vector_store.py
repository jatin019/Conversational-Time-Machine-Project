from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

def load_vector_store(persona: str):
    if persona.lower() == "indira":
        path = "data/faiss_indira"
    else:
        path = "data/faiss_atal"
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
