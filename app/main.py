from fastapi import FastAPI, HTTPException
from app.models import DocumentUpload, QueryRequest, QueryResponse

app = FastAPI(
    title="ContextCoach API",
    description="Backend service for RAG-powered personal development and coaching workflows.",
    version="1.0.0"
)

# In-memory store placeholder for our documents
document_store = []

# Start of API endpoints
@app.get("/")
def read_root():
    """Health check endpoint to verify the API is running."""
    return {"status": "healthy", "service": "ContextCoach API"}

@app.post("/api/upload", status_code=201)
def upload_document(doc: DocumentUpload):
    """
    Simulates ingesting a document, splitting it, and saving it.
    """
    if not doc.content.strip():
        raise HTTPException(status_code=400, detail="Document content cannot be empty.")
    
    document_store.append({"title": doc.title, "content": doc.content})
    return {
        "message": "Document successfully ingested and indexed.",
        "title": doc.title,
        "total_stored_docs": len(document_store)
    }

@app.post("/api/chat", response_model=QueryResponse)
def chat_with_coach(query: QueryRequest):
    """
    Simulates a RAG workflow: searches stored documents for relevance 
    and returns a structured coaching response.
    """
    if not document_store:
        return QueryResponse(
            answer=f"Hello! I am your AI growth coach. You asked: '{query.question}'. Please upload some background notes first!",
            sources=[]
        )
    
    relevant_sources = []
    matched_contexts = []
    
    for doc in document_store:
        if any(word.lower() in doc["content"].lower() for word in query.question.split()):
            matched_contexts.append(doc["content"])
            relevant_sources.append(doc["title"])
            
    if not matched_contexts:
        matched_contexts = [document_store[-1]["content"]]
        relevant_sources = [document_store[-1]["title"]]

    simulated_answer = (
        f"Based on your notes (Source: {', '.join(relevant_sources)}), here is your coaching insight: "
        f"Keep focusing on consistent execution regarding '{query.question}'. Break your goals into milestones!"
    )

    return QueryResponse(
        answer=simulated_answer,
        sources=relevant_sources
    )