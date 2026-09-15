import os
import shutil
from fastapi.testclient import TestClient
from app.main import app
from app.services import vector_service

# Initialize the test client using our FastAPI app instance
client = TestClient(app)

def teardown_module(module):
    """Clean up the local persistent chroma_db directory after tests finish."""
    if os.path.exists(vector_service.persist_directory):
        shutil.rmtree(vector_service.persist_directory)

def test_read_root():
    """Test the root health check endpoint and verify vector DB status."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "ContextCoach API"
    assert data["vector_db"] == "Active"

def test_upload_document():
    """Test uploading a new coaching note/document to ChromaDB."""
    payload = {
        "title": "Time Management Strategy",
        "content": "Focus on deep work blocks of 90 minutes to maximize personal productivity."
    }
    response = client.post("/api/upload", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Time Management Strategy"
    assert "successfully embedded and indexed" in data["message"]
    assert "document_id" in data

def test_chat_with_coach_vector_search():
    """Test the chat/RAG vector search endpoint after uploading relevant context."""
    # First, upload a document to ensure the vector collection has content
    client.post("/api/upload", json={
        "title": "Leadership Goals",
        "content": "Effective leadership requires active listening and consistent team feedback."
    })

    # Test querying the chat endpoint using semantic context
    chat_payload = {
        "question": "How do I become a better leader?"
    }
    response = client.post("/api/chat", json=chat_payload)
    assert response.status_code == 200
    data = response.json()
    
    # Verify the structure matches our QueryResponse model
    assert "answer" in data
    assert "sources" in data
    assert "Leadership Goals" in data["sources"]