import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import PyPDF2


# Paths
pdf_path = "data/Indira_Gandhi.pdf"
speeches_path = "data/speeches.txt"
quotes_path = "data/quotes.txt"
output_path = "data/faiss_indira"

# pdf_path = "data/Atal_Bihari_Vajpayee.pdf"
# speeches_path = "data/atal g speeches.txt"
# quotes_path = "data/atal g quotes.txt"
# output_path = "data/faiss_atal" 

# Extracted the text from PDF
def extract_pdf_text(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

# speeches and quotes
def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

pdf_text = extract_pdf_text(pdf_path)
speeches_text = read_file(speeches_path)
quotes_text = read_file(quotes_path)

# Combineed all text in one 
combined_text = pdf_text + "\n\n" + speeches_text + "\n\n" + quotes_text

# Split into smaller chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_text(combined_text)

# Generate embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Created FAISS vector store
vectorstore = FAISS.from_texts(docs, embeddings)
vectorstore.save_local(output_path)

print(f"Vector store created at {output_path} with {len(docs)} chunks.")
