"""
Integration tests for API endpoints.
"""

import pytest
import json
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock

from src.lvbk.api.main import create_app


class TestAPI:
    """Integration tests for API endpoints."""
    
    def setup_method(self):
        """Set up test client."""
        self.app = create_app()
        self.client = TestClient(self.app)
    
    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = self.client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "0.1.0"
        assert data["service"] == "LVBK API"
    
    def test_root_endpoint(self):
        """Test root endpoint."""
        response = self.client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data
        assert "health" in data
    
    def test_get_supported_martial_arts(self):
        """Test getting supported martial arts."""
        response = self.client.get("/api/martial_arts")
        
        assert response.status_code == 200
        data = response.json()
        assert "martial_arts" in data
        assert len(data["martial_arts"]) == 4
        
        # Check martial arts structure
        for art in data["martial_arts"]:
            assert "id" in art
            assert "name" in art
            assert "description" in art
            assert "techniques" in art
    
    def test_analyze_technique_missing_file(self):
        """Test analyze endpoint with missing file."""
        response = self.client.post(
            "/api/analyze",
            data={"martial_art": "silat_lincah"}
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_analyze_technique_invalid_martial_art(self):
        """Test analyze endpoint with invalid martial art."""
        fake_video = ("test.mp4", b"fake_video_data", "video/mp4")
        
        response = self.client.post(
            "/api/analyze",
            files={"video": fake_video},
            data={"martial_art": "invalid_art"}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "Unsupported martial art" in data["detail"]
    
    def test_analyze_technique_file_too_large(self):
        """Test analyze endpoint with file too large."""
        # Create fake large video data (1GB + 1 byte)
        large_video_data = b"x" * (1024 * 1024 * 1024 + 1)
        fake_video = ("test.mp4", large_video_data, "video/mp4")
        
        response = self.client.post(
            "/api/analyze",
            files={"video": fake_video},
            data={"martial_art": "silat_lincah"}
        )
        
        assert response.status_code == 413
        data = response.json()
        assert "File too large" in data["detail"]
    
    @patch('src.lvbk.api.endpoints.process_video_analysis')
    def test_analyze_technique_success(self, mock_process):
        """Test successful technique analysis."""
        fake_video = ("test.mp4", b"fake_video_data", "video/mp4")
        
        response = self.client.post(
            "/api/analyze",
            files={"video": fake_video},
            data={"martial_art": "silat_lincah", "confidence_threshold": "0.8"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "analysis_id" in data
        assert data["status"] == "processing"
        assert "message" in data
    
    def test_get_analysis_result_not_found(self):
        """Test getting analysis result that doesn't exist."""
        fake_id = "nonexistent-id"
        
        response = self.client.get(f"/api/analysis/{fake_id}")
        
        assert response.status_code == 404
        data = response.json()
        assert "Analysis not found" in data["detail"]
    
    def test_list_analyses_empty(self):
        """Test listing analyses when none exist."""
        response = self.client.get("/api/analysis")
        
        assert response.status_code == 200
        data = response.json()
        assert data["analyses"] == []
        assert data["total"] == 0
        assert data["limit"] == 10
        assert data["offset"] == 0
        assert data["has_more"] == False
    
    def test_list_analyses_with_limit_and_offset(self):
        """Test listing analyses with pagination."""
        response = self.client.get("/api/analysis?limit=5&offset=0")
        
        assert response.status_code == 200
        data = response.json()
        assert data["limit"] == 5
        assert data["offset"] == 0
    
    def test_list_analyses_with_martial_art_filter(self):
        """Test listing analyses with martial art filter."""
        response = self.client.get("/api/analysis?martial_art=silat_lincah")
        
        assert response.status_code == 200
        data = response.json()
        assert "analyses" in data
    
    def test_delete_analysis_not_found(self):
        """Test deleting analysis that doesn't exist."""
        fake_id = "nonexistent-id"
        
        response = self.client.delete(f"/api/analysis/{fake_id}")
        
        assert response.status_code == 404
        data = response.json()
        assert "Analysis not found" in data["detail"]
    
    def test_api_documentation_endpoints(self):
        """Test API documentation endpoints."""
        # Test OpenAPI JSON
        response = self.client.get("/openapi.json")
        assert response.status_code == 200
        
        # Test Swagger UI
        response = self.client.get("/docs")
        assert response.status_code == 200
        
        # Test ReDoc
        response = self.client.get("/redoc")
        assert response.status_code == 200





