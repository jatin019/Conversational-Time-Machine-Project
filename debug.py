"""
Debug script to check dependency versions and compatibility
"""

import sys
import warnings

def check_dependencies():
    print("🔍 Checking dependency versions...")
    
    try:
        import numpy as np
        print(f"✅ NumPy: {np.__version__}")
    except ImportError as e:
        print(f"❌ NumPy not found: {e}")
    
    try:
        import sentence_transformers
        print(f"✅ Sentence Transformers: {sentence_transformers.__version__}")
    except ImportError as e:
        print(f"❌ Sentence Transformers not found: {e}")
    except Exception as e:
        print(f"⚠️  Sentence Transformers import issue: {e}")
    
    try:
        import faiss
        print(f"✅ FAISS: Version available")
    except ImportError as e:
        print(f"❌ FAISS not found: {e}")
    
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        print(f"✅ LangChain HuggingFaceEmbeddings: Available")
    except ImportError as e:
        print(f"❌ LangChain HuggingFaceEmbeddings not found: {e}")
    except Exception as e:
        print(f"⚠️  LangChain HuggingFaceEmbeddings issue: {e}")
    
    try:
        from langchain_community.vectorstores import FAISS
        print(f"✅ LangChain FAISS: Available")
    except ImportError as e:
        print(f"❌ LangChain FAISS not found: {e}")

def test_embeddings():
    print("\n🧪 Testing embeddings initialization...")
    
    try:
        # Suppress warnings
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        
        from langchain_community.embeddings import HuggingFaceEmbeddings
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        print("✅ Embeddings initialized successfully")
        
        # Test encoding
        test_text = ["Hello world", "This is a test"]
        encoded = embeddings.embed_documents(test_text)
        print(f"✅ Embeddings test successful: {len(encoded)} vectors, {len(encoded[0])} dimensions")
        
    except Exception as e:
        print(f"❌ Embeddings test failed: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()

def test_vector_store_loading():
    print("\n📚 Testing vector store loading...")
    
    try:
        from backend.utils.vector_store import load_vector_store
        
        # Test Atal
        try:
            vs_atal = load_vector_store("atal")
            print("✅ Atal vector store loaded successfully")
        except Exception as e:
            print(f"❌ Atal vector store failed: {e}")
        
        # Test Indira
        try:
            vs_indira = load_vector_store("indira")
            print("✅ Indira vector store loaded successfully")
        except Exception as e:
            print(f"❌ Indira vector store failed: {e}")
            
    except Exception as e:
        print(f"❌ Vector store loading test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Starting dependency debug...")
    check_dependencies()
    test_embeddings()
    test_vector_store_loading()
    print("\n🏁 Debug complete!")