# backend/utils/vector_store.py
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from pathlib import Path
import os

def load_vector_store(persona: str):
    persona = persona.lower().strip()
    
    # Get absolute path - works on both Windows and Linux
    current_file = Path(__file__).resolve()  # /app/backend/utils/vector_store.py
    project_root = current_file.parent.parent.parent  # /app/
    
    if persona == "indira":
        path = project_root / "backend" / "data" / "faiss_indira"
    elif persona == "atal":
        path = project_root / "backend" / "data" / "faiss_atal"
    else:
        raise ValueError(f"Unknown persona '{persona}'. Expected 'atal' or 'indira'.")

    print(f"🧠 Loading vector store from: {path}")
    print(f"📂 Path exists: {path.exists()}")
    print(f"📂 Current working directory: {os.getcwd()}")
    print(f"📂 File location: {current_file}")
    print(f"📂 Project root: {project_root}")
    
    # Debug: Check if parent directories exist
    if not path.parent.exists():
        print(f"❌ Parent directory missing: {path.parent}")
        print(f"📂 Backend directory contents: {list((project_root / 'backend').glob('*')) if (project_root / 'backend').exists() else 'Backend dir not found'}")
    
    if not path.exists():
        print(f"❌ Vector store directory not found: {path}")
        # Try alternative paths
        alt_path1 = Path("backend/data") / f"faiss_{persona}"
        alt_path2 = Path("./backend/data") / f"faiss_{persona}"
        alt_path3 = Path(os.getcwd()) / "backend" / "data" / f"faiss_{persona}"
        
        print(f"🔍 Trying alternative paths:")
        print(f"   Alt 1: {alt_path1} - exists: {alt_path1.exists()}")
        print(f"   Alt 2: {alt_path2} - exists: {alt_path2.exists()}")
        print(f"   Alt 3: {alt_path3} - exists: {alt_path3.exists()}")
        
        # Use working alternative
        if alt_path1.exists():
            path = alt_path1
        elif alt_path2.exists():
            path = alt_path2
        elif alt_path3.exists():
            path = alt_path3
        else:
            raise FileNotFoundError(f"Vector store not found at any path. Tried: {path}, {alt_path1}, {alt_path2}, {alt_path3}")
    
    # Check required files exist
    faiss_file = path / "index.faiss"
    pkl_file = path / "index.pkl"
    
    if not faiss_file.exists():
        raise FileNotFoundError(f"FAISS index file missing: {faiss_file}")
    if not pkl_file.exists():
        raise FileNotFoundError(f"PKL file missing: {pkl_file}")
    
    print(f"📂 Contents: {list(path.glob('*'))}")
    print(f"📊 FAISS file size: {faiss_file.stat().st_size} bytes")
    print(f"📊 PKL file size: {pkl_file.stat().st_size} bytes")

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Convert to string for FAISS (required on some systems)
    return FAISS.load_local(str(path), embeddings, allow_dangerous_deserialization=True)
