import os
from pathlib import Path
import faiss
import pickle

def debug_faiss_files():
    """Debug FAISS files to understand the corruption"""
    
    personas = ['indira', 'atal']
    
    for persona in personas:
        print(f"\n=== Debugging {persona.upper()} ===")
        
        # Check paths
        faiss_dir = Path(f"backend/data/faiss_{persona}")
        faiss_file = faiss_dir / "index.faiss" 
        pkl_file = faiss_dir / "index.pkl"
        
        print(f"📂 Directory: {faiss_dir}")
        print(f"📂 Directory exists: {faiss_dir.exists()}")
        print(f"📄 FAISS file exists: {faiss_file.exists()}")
        print(f"📄 PKL file exists: {pkl_file.exists()}")
        
        if faiss_file.exists():
            size = faiss_file.stat().st_size
            print(f"📊 FAISS file size: {size} bytes")
            
            # Try to read first few bytes
            try:
                with open(faiss_file, 'rb') as f:
                    header = f.read(20)  # Read first 20 bytes
                print(f"🔍 File header (hex): {header.hex()}")
                print(f"🔍 File header (ascii): {header}")
                
                # Try to load with FAISS
                try:
                    index = faiss.read_index(str(faiss_file))
                    print(f"✅ FAISS index loaded successfully")
                    print(f"📊 Index dimension: {index.d}")
                    print(f"📊 Index count: {index.ntotal}")
                except Exception as e:
                    print(f"❌ FAISS load error: {e}")
                    
            except Exception as e:
                print(f"❌ File read error: {e}")
        
        if pkl_file.exists():
            size = pkl_file.stat().st_size  
            print(f"📊 PKL file size: {size} bytes")
            
            try:
                with open(pkl_file, 'rb') as f:
                    data = pickle.load(f)
                print(f"✅ PKL file loaded successfully")
                print(f"📊 PKL keys: {list(data.keys()) if isinstance(data, dict) else type(data)}")
            except Exception as e:
                print(f"❌ PKL load error: {e}")

if __name__ == "__main__":
    debug_faiss_files()
