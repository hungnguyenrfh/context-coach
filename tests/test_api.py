from fastapi.testclient import TestClient
from app.main import app

# Initialize the test client using our FastAPI app instance
client = TestClient(app)

def test_read_root():
    """Test the root health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "ContextCoach API"}

def test_upload_document():
    """Test uploading a new coaching note/document."""
    payload = {
        "title": "Time Management Strategy",
        "content": "Focus on deep work blocks of 90 minutes to maximize personal productivity."
    }
    response = client.post("/api/upload", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Time Management Strategy"
    assert "successfully ingested" in data["message"]

def test_chat_with_coach():
    """Test the chat/RAG endpoint after a document has been uploaded."""
    # First, ensure a document is uploaded so context exists
    client.post("/api/upload", json={
        "title": "Leadership Goals",
        "content": "Effective leadership requires active listening and consistent team feedback."
    })

    # Now test the chat endpoint
    chat_payload = {
        "question": "How do I improve leadership?"
    }
    response = client.post("/api/chat", json=chat_payload)
    assert response.status_code == 200
    data = response.json()
    
    # Verify the structure matches our QueryResponse model
    assert "answer" in data
    assert "sources" in data
    assert "Leadership Goals" in data["sources"]