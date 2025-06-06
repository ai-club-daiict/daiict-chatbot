import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# 🔹 Path to your extracted folder (update this!)
scraped_folder = "/Users/meetgandhi/Desktop/A/scraped_data"  # <- change this as needed

# 🔹 Load all valid .txt files recursively
all_documents = []
for root, _, files in os.walk(scraped_folder):
    for file in files:
        if file.endswith(".txt"):
            file_path = os.path.join(root, file)
            try:
                loader = TextLoader(file_path)
                documents = loader.load()
                if documents:  # Only include non-empty
                    all_documents.extend(documents)
            except Exception as e:
                print(f"⚠️ Skipping {file_path} due to error: {e}")

# 🧩 Split into text chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
all_chunks = text_splitter.split_documents(all_documents)

# ✅ Safety check
if not all_chunks:
    raise ValueError("No valid text chunks found. Check if your files contain readable content.")

# 🔍 Generate embeddings using HuggingFace
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 📦 Create FAISS vector store and save it
vectorstore = FAISS.from_documents(all_chunks, embedding)
vectorstore.save_local("multi_file_vector_index")

print("✅ Vector store created and saved to ./multi_file_vector_index")
