from fastapi import FastAPI
from pydantic import BaseModel
from rag_chain import ask_question
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

@app.post("/chat")
def chat(query: Query):
    response = ask_question(query.question)
    return {"answer": response["result"], "sources": [doc.metadata for doc in response["source_documents"]]}