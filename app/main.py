from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import uuid

from app.models import DocumentUpload, QueryRequest, QueryResponse
from app.services import vector_service

app = FastAPI(
    title="ContextCoach API",
    description="Backend service with ChromaDB vector search for RAG-powered personal coaching workflows.",
    version="2.0.0"
)

# Serve the static frontend folder
app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root():
    """Serves the frontend dashboard UI."""
    html_path = Path(__file__).parent / "static" / "index.html"
    return html_path.read_text(encoding="utf-8")

@app.post("/api/upload", status_code=201)
def upload_document(doc: DocumentUpload):
    if not doc.content.strip():
        raise HTTPException(status_code=400, detail="Document content cannot be empty.")
    
    doc_id = str(uuid.uuid4())
    vector_service.add_document(doc_id=doc_id, title=doc.title, content=doc.content)
    
    return {
        "message": "Document successfully embedded and indexed in ChromaDB.",
        "title": doc.title,
        "document_id": doc_id
    }

@app.post("/api/chat", response_model=QueryResponse)
def chat_with_coach(query: QueryRequest):
    search_results = vector_service.query_similar(query_text=query.question)
    
    if not search_results["contexts"]:
        return QueryResponse(
            answer=f"Hello! I am your AI growth coach. You asked: '{query.question}'. Please upload some background notes first!",
            sources=[]
        )
    
    matched_contexts = search_results["contexts"]
    relevant_sources = list(set(search_results["sources"]))

    simulated_answer = (
        f"Based on semantic vector search (Sources: {', '.join(relevant_sources)}), here is your coaching insight: "
        f"To address '{query.question}', prioritize alignment with your core notes: '{matched_contexts[0][:100]}...'"
    )

    return QueryResponse(
        answer=simulated_answer,
        sources=relevant_sources
    )