"""
Tests for FastAPI endpoints
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestAPIEndpoints:
    """Test cases for API endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns expected response"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["status"] == "running"
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "documents_indexed" in data
        assert data["status"] == "healthy"
    
    def test_status_endpoint(self):
        """Test status endpoint"""
        response = client.get("/status")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "message" in data
        assert "document_count" in data
    
    def test_chat_without_documents(self):
        """Test chat endpoint when no documents are uploaded"""
        response = client.post(
            "/chat",
            json={"query": "What is machine learning?"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "sources" in data
        # Should prompt to upload materials
        assert "upload" in data["answer"].lower() or "materials" in data["answer"].lower()
    
    def test_chat_empty_query(self):
        """Test chat endpoint with empty query"""
        response = client.post(
            "/chat",
            json={"query": ""}
        )
        
        assert response.status_code == 400
    
    def test_chat_with_history(self):
        """Test chat endpoint with conversation history"""
        response = client.post(
            "/chat",
            json={
                "query": "Tell me more",
                "chat_history": [
                    {"role": "user", "content": "What is Python?"},
                    {"role": "assistant", "content": "Python is a programming language."}
                ]
            }
        )
        
        # Should succeed even without documents (will prompt to upload)
        assert response.status_code == 200
    
    def test_upload_without_file(self):
        """Test upload endpoint without file"""
        response = client.post("/upload")
        
        assert response.status_code == 422  # Unprocessable Entity
    
    def test_clear_endpoint(self):
        """Test clear documents endpoint"""
        response = client.delete("/clear")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
