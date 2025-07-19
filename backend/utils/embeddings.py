import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import PyPDF2

# Paths for Atal's data
pdf_path = "data/Atal_Bihari_Vajpayee.pdf"  # Replace with your Atal PDF
speeches_path = "data/atal g speeches.txt"    # Replace with Atal speeches file
quotes_path = "data/atal g quotes.txt"        # Replace with Atal quotes file
output_path = "data/faiss_atal"

# 1. Extract text from PDF
def extract_pdf_text(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

# 2. Read speeches and quotes
def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# Extract data
pdf_text = extract_pdf_text(pdf_path)
speeches_text = read_file(speeches_path)
quotes_text = read_file(quotes_path)

# 3. Combine all text
combined_text = pdf_text + "\n\n" + speeches_text + "\n\n" + quotes_text

# 4. Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_text(combined_text)

# 5. Generate embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 6. Create FAISS vector store
vectorstore = FAISS.from_texts(docs, embeddings)
vectorstore.save_local(output_path)

print(f"✅ Vector store created at {output_path} with {len(docs)} chunks for Atal Bihari Vajpayee.")
