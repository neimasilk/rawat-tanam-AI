import pytest
import asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
import io
from PIL import Image
import json
import time

# Import the main app
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from config import settings

# Test client
client = TestClient(app)

class TestHealthCheck:
    """Test health check endpoint"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == settings.PROJECT_NAME
        assert "timestamp" in data

class TestAPIInfo:
    """Test API info endpoints"""
    
    def test_api_info(self):
        """Test API info endpoint"""
        response = client.get("/api/v1/info")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Rawat Tanam AI API"
        assert "endpoints" in data
        assert "documentation" in data

class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_register_user(self):
        """Test user registration"""
        user_data = {
            "email": f"test_{int(time.time())}@example.com",
            "password": "testpassword123",
            "full_name": "Test User",
            "organization": "Test Organization",
            "intended_use": "Testing purposes"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user_info" in data
        assert data["user_info"]["email"] == user_data["email"]
    
    def test_login_user(self):
        """Test user login with demo credentials"""
        login_data = {
            "email": "demo@rawat-tanam-ai.com",
            "password": "demo123"
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user_info"]["email"] == login_data["email"]
    
    def test_get_tiers(self):
        """Test get available tiers"""
        response = client.get("/api/v1/auth/tiers")
        assert response.status_code == 200
        data = response.json()
        assert "tiers" in data
        assert "free" in data["tiers"]
        assert "professional" in data["tiers"]
        assert "enterprise" in data["tiers"]
        assert "partner" in data["tiers"]

class TestSpeciesAPI:
    """Test species database endpoints"""
    
    def test_list_species(self):
        """Test species listing with pagination"""
        headers = {"X-API-Key": "free_demo_key_123"}
        response = client.get("/api/v1/species/?page=1&per_page=5", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "species" in data
        assert "total" in data
        assert "page" in data
        assert "per_page" in data
        assert len(data["species"]) <= 5
    
    def test_get_species_by_id(self):
        """Test getting specific species by ID"""
        headers = {"X-API-Key": "free_demo_key_123"}
        response = client.get("/api/v1/species/ficus_benjamina", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["species_id"] == "ficus_benjamina"
        assert data["scientific_name"] == "Ficus benjamina"
        assert "family" in data
        assert "genus" in data
    
    def test_search_species(self):
        """Test species search functionality"""
        headers = {"X-API-Key": "free_demo_key_123"}
        response = client.get("/api/v1/species/search/?q=ficus&limit=5", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert "query" in data
        assert data["query"] == "ficus"
        assert "search_time" in data
    
    def test_get_families(self):
        """Test getting plant families list"""
        headers = {"X-API-Key": "free_demo_key_123"}
        response = client.get("/api/v1/species/families/list", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "families" in data
        assert "family_counts" in data
        assert "total_families" in data
    
    def test_get_database_stats(self):
        """Test getting database statistics"""
        headers = {"X-API-Key": "free_demo_key_123"}
        response = client.get("/api/v1/species/stats", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "total_species" in data
        assert "total_families" in data
        assert "total_genera" in data
        assert "database_version" in data

class TestIdentificationAPI:
    """Test plant identification endpoints"""
    
    def create_test_image(self) -> io.BytesIO:
        """Create a test image for upload"""
        # Create a simple test image
        img = Image.new('RGB', (100, 100), color='green')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        return img_bytes
    
    def test_identify_plant(self):
        """Test plant identification with image upload"""
        headers = {"X-API-Key": "free_demo_key_123"}
        
        # Create test image
        test_image = self.create_test_image()
        
        files = {"file": ("test_plant.jpg", test_image, "image/jpeg")}
        response = client.post("/api/v1/identify/", headers=headers, files=files)
        
        assert response.status_code == 200
        data = response.json()
        assert "request_id" in data
        assert "results" in data
        assert "processing_time" in data
        assert "image_info" in data
        assert "metadata" in data
        
        # Check if results contain expected fields
        if data["results"]:
            result = data["results"][0]
            assert "species_id" in result
            assert "scientific_name" in result
            assert "confidence" in result
            assert "family" in result
    
    def test_identify_status(self):
        """Test identification service status"""
        headers = {"X-API-Key": "free_demo_key_123"}
        response = client.get("/api/v1/identify/status", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "Plant Identification"
        assert data["status"] == "operational"
        assert "supported_formats" in data
        assert "confidence_threshold" in data

class TestRateLimiting:
    """Test rate limiting functionality"""
    
    def test_rate_limiting_headers(self):
        """Test that rate limiting headers are present"""
        headers = {"X-API-Key": "free_demo_key_123"}
        response = client.get("/api/v1/species/stats", headers=headers)
        
        assert response.status_code == 200
        assert "X-RateLimit-Limit" in response.headers
        assert "X-RateLimit-Remaining" in response.headers
        assert "X-RateLimit-Reset" in response.headers
        assert "X-RateLimit-Tier" in response.headers
    
    def test_different_tier_limits(self):
        """Test different API key tiers have different limits"""
        # Test free tier
        free_headers = {"X-API-Key": "free_demo_key_123"}
        free_response = client.get("/api/v1/species/stats", headers=free_headers)
        assert free_response.headers["X-RateLimit-Tier"] == "free"
        
        # Test professional tier
        pro_headers = {"X-API-Key": "professional_key_456"}
        pro_response = client.get("/api/v1/species/stats", headers=pro_headers)
        assert pro_response.headers["X-RateLimit-Tier"] == "professional"

class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_unauthorized_access(self):
        """Test accessing protected endpoint without authentication"""
        response = client.get("/api/v1/species/stats")
        assert response.status_code == 401
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == 401
    
    def test_invalid_api_key(self):
        """Test using invalid API key"""
        headers = {"X-API-Key": "invalid_key_123"}
        response = client.get("/api/v1/species/stats", headers=headers)
        assert response.status_code == 401
    
    def test_species_not_found(self):
        """Test getting non-existent species"""
        headers = {"X-API-Key": "free_demo_key_123"}
        response = client.get("/api/v1/species/nonexistent_species", headers=headers)
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
    
    def test_invalid_image_upload(self):
        """Test uploading invalid file type"""
        headers = {"X-API-Key": "free_demo_key_123"}
        
        # Create a text file instead of image
        text_file = io.BytesIO(b"This is not an image")
        files = {"file": ("test.txt", text_file, "text/plain")}
        
        response = client.post("/api/v1/identify/", headers=headers, files=files)
        assert response.status_code == 400

class TestIntegration:
    """Test integration functionality"""
    
    @pytest.mark.asyncio
    async def test_tanam_rawat_integration(self):
        """Test Tanam Rawat integration (mock)"""
        from integrations.tanam_rawat_client import test_integration
        
        # This will test the mock integration
        result = await test_integration()
        assert "health_check" in result
        assert "search_test" in result
        assert "integration_status" in result

if __name__ == "__main__":
    # Run tests
    pytest.main(["-v", __file__])