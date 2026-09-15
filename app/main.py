import uuid
from fastapi import FastAPI, HTTPException
from app.models import DocumentUpload, QueryRequest, QueryResponse
from app.services import vector_service

app = FastAPI(
    title="ContextCoach API",
    description="Backend service with ChromaDB vector search for RAG-powered personal coaching workflows.",
    version="2.0.0"
)

@app.get("/")
def read_root():
    """Health check endpoint to verify the API is running."""
    return {"status": "healthy", "service": "ContextCoach API", "vector_db": "Active"}

@app.post("/api/upload", status_code=201)
def upload_document(doc: DocumentUpload):
    """
    Ingests a document, generates vector embeddings, and stores it in ChromaDB.
    """
    if not doc.content.strip():
        raise HTTPException(status_code=400, detail="Document content cannot be empty.")
    
    # Generate a unique ID for the document chunk
    doc_id = str(uuid.uuid4())
    
    # Store in ChromaDB
    vector_service.add_document(doc_id=doc_id, title=doc.title, content=doc.content)
    
    return {
        "message": "Document successfully embedded and indexed in ChromaDB.",
        "title": doc.title,
        "document_id": doc_id
    }

@app.post("/api/chat", response_model=QueryResponse)
def chat_with_coach(query: QueryRequest):
    """
    Performs a true RAG vector search against ChromaDB and returns a structured coaching response.
    """
    search_results = vector_service.query_similar(query_text=query.question)
    
    if not search_results["contexts"]:
        return QueryResponse(
            answer=f"Hello! I am your AI growth coach. You asked: '{query.question}'. Please upload some background notes first!",
            sources=[]
        )
    
    matched_contexts = search_results["contexts"]
    relevant_sources = list(set(search_results["sources"])) # Deduplicate sources

    simulated_answer = (
        f"Based on semantic vector search (Sources: {', '.join(relevant_sources)}), here is your coaching insight: "
        f"To address '{query.question}', prioritize alignment with your core notes: '{matched_contexts[0][:100]}...'"
    )

    return QueryResponse(
        answer=simulated_answer,
        sources=relevant_sources
    )