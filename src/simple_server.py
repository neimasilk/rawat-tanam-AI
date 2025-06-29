#!/usr/bin/env python3
"""
Simple FastAPI server untuk testing tanpa dependencies kompleks
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, Any, List

try:
    from fastapi import FastAPI, HTTPException, Request, Response
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
except ImportError:
    print("FastAPI not installed. Please install with: pip install fastapi uvicorn")
    exit(1)

# Simple configuration
class SimpleConfig:
    PROJECT_NAME = "Rawat Tanam AI API"
    VERSION = "1.0.0"
    API_V1_STR = "/api/v1"
    DEBUG = True
    HOST = "0.0.0.0"
    PORT = 8000

config = SimpleConfig()

# Create FastAPI app
app = FastAPI(
    title=config.PROJECT_NAME,
    version=config.VERSION,
    description="Indonesian Flora Identification API Platform",
    debug=config.DEBUG
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data
MOCK_SPECIES = [
    {
        "species_id": "ficus_benjamina",
        "scientific_name": "Ficus benjamina",
        "common_names": ["Beringin", "Ficus"],
        "family": "Moraceae",
        "genus": "Ficus",
        "description": "Pohon hias populer dengan daun mengkilap",
        "native_to": "Indonesia",
        "care_level": "Easy"
    },
    {
        "species_id": "dendrobium_nobile",
        "scientific_name": "Dendrobium nobile",
        "common_names": ["Anggrek Dendrobium", "Noble Dendrobium"],
        "family": "Orchidaceae",
        "genus": "Dendrobium",
        "description": "Anggrek epifit dengan bunga cantik",
        "native_to": "Indonesia",
        "care_level": "Intermediate"
    },
    {
        "species_id": "monstera_deliciosa",
        "scientific_name": "Monstera deliciosa",
        "common_names": ["Janda Bolong", "Swiss Cheese Plant"],
        "family": "Araceae",
        "genus": "Monstera",
        "description": "Tanaman hias dengan daun berlubang unik",
        "native_to": "Central America",
        "care_level": "Easy"
    }
]

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": config.PROJECT_NAME,
        "version": config.VERSION,
        "timestamp": datetime.now().isoformat(),
        "uptime": "running"
    }

# API Info endpoint
@app.get(f"{config.API_V1_STR}/info")
async def api_info():
    return {
        "name": "Rawat Tanam AI API",
        "version": config.VERSION,
        "description": "Indonesian Flora Identification API",
        "endpoints": {
            "health": "/health",
            "species": f"{config.API_V1_STR}/species/",
            "identify": f"{config.API_V1_STR}/identify/",
            "auth": f"{config.API_V1_STR}/auth/"
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "status": "operational"
    }

# Species endpoints
@app.get(f"{config.API_V1_STR}/species/")
async def list_species(page: int = 1, per_page: int = 10, family: str = None):
    """List species with pagination"""
    filtered_species = MOCK_SPECIES
    if family:
        filtered_species = [s for s in MOCK_SPECIES if s["family"].lower() == family.lower()]
    
    total = len(filtered_species)
    start = (page - 1) * per_page
    end = start + per_page
    species_page = filtered_species[start:end]
    
    return {
        "species": species_page,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page
    }

@app.get(f"{config.API_V1_STR}/species/{{species_id}}")
async def get_species(species_id: str):
    """Get specific species by ID"""
    species = next((s for s in MOCK_SPECIES if s["species_id"] == species_id), None)
    if not species:
        raise HTTPException(status_code=404, detail="Species not found")
    return species

@app.get(f"{config.API_V1_STR}/species/search/")
async def search_species(q: str, limit: int = 10):
    """Search species by name"""
    start_time = time.time()
    
    results = []
    query_lower = q.lower()
    
    for species in MOCK_SPECIES:
        if (query_lower in species["scientific_name"].lower() or 
            any(query_lower in name.lower() for name in species["common_names"])):
            results.append(species)
    
    results = results[:limit]
    search_time = time.time() - start_time
    
    return {
        "results": results,
        "query": q,
        "total_found": len(results),
        "search_time": round(search_time, 3)
    }

@app.get(f"{config.API_V1_STR}/species/stats")
async def get_database_stats():
    """Get database statistics"""
    families = list(set(s["family"] for s in MOCK_SPECIES))
    genera = list(set(s["genus"] for s in MOCK_SPECIES))
    
    return {
        "total_species": len(MOCK_SPECIES),
        "total_families": len(families),
        "total_genera": len(genera),
        "database_version": "1.0.0",
        "last_updated": "2024-01-15",
        "coverage": "Indonesian Flora (Sample)"
    }

# Simple identification endpoint
@app.post(f"{config.API_V1_STR}/identify/")
async def identify_plant():
    """Mock plant identification"""
    # Simulate processing time
    processing_time = 1.2
    
    # Mock identification result
    result = {
        "request_id": f"req_{int(time.time())}",
        "results": [
            {
                "species_id": "ficus_benjamina",
                "scientific_name": "Ficus benjamina",
                "common_names": ["Beringin", "Ficus"],
                "confidence": 0.92,
                "family": "Moraceae",
                "genus": "Ficus"
            },
            {
                "species_id": "monstera_deliciosa",
                "scientific_name": "Monstera deliciosa",
                "common_names": ["Janda Bolong"],
                "confidence": 0.78,
                "family": "Araceae",
                "genus": "Monstera"
            }
        ],
        "processing_time": processing_time,
        "image_info": {
            "format": "JPEG",
            "width": 1024,
            "height": 768,
            "size_bytes": 245760
        },
        "metadata": {
            "model_version": "v1.0.0",
            "confidence_threshold": 0.7,
            "timestamp": datetime.now().isoformat()
        }
    }
    
    return result

@app.get(f"{config.API_V1_STR}/identify/status")
async def identify_status():
    """Get identification service status"""
    return {
        "service": "Plant Identification",
        "status": "operational",
        "model_loaded": True,
        "supported_formats": ["JPEG", "PNG", "WebP"],
        "max_file_size": "10MB",
        "confidence_threshold": 0.7,
        "average_processing_time": "1.2s"
    }

# Simple auth endpoints
@app.post(f"{config.API_V1_STR}/auth/register")
async def register():
    """Mock user registration"""
    return {
        "message": "User registered successfully",
        "user_id": f"user_{int(time.time())}",
        "api_key": f"demo_key_{int(time.time())}",
        "tier": "free"
    }

@app.post(f"{config.API_V1_STR}/auth/login")
async def login():
    """Mock user login"""
    return {
        "access_token": f"token_{int(time.time())}",
        "token_type": "bearer",
        "expires_in": 3600,
        "user_info": {
            "email": "demo@rawat-tanam-ai.com",
            "tier": "free"
        }
    }

@app.get(f"{config.API_V1_STR}/auth/tiers")
async def get_tiers():
    """Get available API tiers"""
    return {
        "tiers": {
            "free": {
                "name": "Free",
                "rate_limit": "100/hour",
                "features": ["Basic identification", "Limited species database"]
            },
            "professional": {
                "name": "Professional",
                "rate_limit": "1000/hour",
                "features": ["Full species database", "Priority support", "Analytics"]
            },
            "enterprise": {
                "name": "Enterprise",
                "rate_limit": "10000/hour",
                "features": ["Custom models", "SLA", "Dedicated support"]
            }
        }
    }

if __name__ == "__main__":
    print(f"🌿 Starting {config.PROJECT_NAME} v{config.VERSION}")
    print(f"📍 Server will run on http://{config.HOST}:{config.PORT}")
    print(f"📚 API Documentation: http://{config.HOST}:{config.PORT}/docs")
    print(f"🔍 Health Check: http://{config.HOST}:{config.PORT}/health")
    
    try:
        import uvicorn
        uvicorn.run(
            "simple_server:app",
            host=config.HOST,
            port=config.PORT,
            reload=config.DEBUG,
            log_level="info"
        )
    except ImportError:
        print("\n❌ uvicorn not installed. Please install with:")
        print("pip install uvicorn")
        print("\nOr run with: uvicorn simple_server:app --reload --host 0.0.0.0 --port 8000")