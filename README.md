# 🎓 DAIICT Chatbot – AI-Powered Admission Assistant

A smart chatbot built for [daiict.ac.in](https://www.daiict.ac.in), designed to answer queries related to admissions, programs, scholarships, placements, and more.

Powered by **LangChain**, **OpenAI**, **ChromaDB**, and **FastAPI**, with a frontend built in **React.js** — this project demonstrates how to implement Retrieval-Augmented Generation (RAG) for educational use cases.

---

## 📁 Project Structure

```
daiict-chatbot/
├── backend/                      # Backend - API, AI logic, document ingestion
│   ├── main.py                   # FastAPI server exposing /chat endpoint
│   ├── rag_chain.py              # LangChain RAG setup with retriever + LLM
│   ├── ingest.py                 # Script to load, chunk & embed PDF content
│   ├── requirements.txt          # Backend dependencies
│   └── data/
│       ├── pdfs/                 # Source documents (DAIICT brochures, etc.)
│       └── chroma/               # Persisted ChromaDB vector store
├── frontend/                     # React frontend for chatbot UI
│   ├── public/
│   ├── src/
│   └── .env                      # API URL (REACT_APP_API_URL)
└── README.md                     # Documentation
```

---

## 🚀 Features

- 🔎 **AI Q&A** using LangChain + OpenAI
- 📄 Ingests long documents (PDFs, web data)
- 🧠 Retrieval-Augmented Generation (RAG)
- 💬 Chat interface (React-based)
- 🧰 Easily extensible and student-friendly
- 🌐 Deploy frontend on Vercel, backend on Render

---

## 🛠️ Tech Stack

| Layer      | Technology                  |
|------------|-----------------------------|
| Frontend   | React.js, Tailwind CSS      |
| Backend    | FastAPI                     |
| NLP Engine | LangChain + OpenAI GPT-3.5  |
| Vector DB  | ChromaDB                    |
| Deployment | Vercel (frontend), Render (backend) |

---

## ⚙️ Setup Instructions

### 🔧 Backend

1. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Add PDFs**
   - Place DAIICT brochures inside `backend/data/pdfs/`

3. **Ingest documents**
   ```bash
   python ingest.py
   ```

4. **Start FastAPI server**
   ```bash
   uvicorn main:app --reload
   ```

### 💻 Frontend

1. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Set API URL**
   Create `.env` file in `frontend/` with:
   ```
   REACT_APP_API_URL=http://localhost:8000/chat
   ```

3. **Run React app**
   ```bash
   npm start
   ```

---

## 🧠 How It Works

- Documents are split into chunks and embedded using OpenAI.
- Embeddings are stored in **ChromaDB**.
- On a query, LangChain retrieves the most relevant chunks.
- A GPT model answers using those chunks (RAG).

---

## ✅ Roadmap

- [ ] Backend API with LangChain RAG
- [ ] ChromaDB document indexing
- [ ] React UI with chat interface
- [ ] Whisper integration for voice input
- [ ] Admin panel for document upload
- [ ] Analytics dashboard (question trends)

---

## 👨‍🎓 For Students

This project is designed to help you learn:

- LangChain pipelines
- RAG architecture
- API development (FastAPI)
- React integration with AI backend
- Vector database usage

---

## 📄 License

This project is intended for educational purposes under the MIT License.
