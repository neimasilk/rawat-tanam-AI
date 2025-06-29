from fastapi import APIRouter, UploadFile, File, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import time
import uuid
from PIL import Image
import io
import logging
from config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

# Response models
class IdentificationResult(BaseModel):
    species_id: str
    scientific_name: str
    common_name: str
    confidence: float
    family: str
    genus: str

class IdentificationResponse(BaseModel):
    request_id: str
    timestamp: float
    results: List[IdentificationResult]
    processing_time: float
    image_info: dict
    metadata: dict

# Mock ML model for demonstration
class MockMLModel:
    def __init__(self):
        # Mock Indonesian plant species data
        self.mock_species = [
            {
                "species_id": "dendrobium_nobile",
                "scientific_name": "Dendrobium nobile",
                "common_name": "Noble Dendrobium",
                "family": "Orchidaceae",
                "genus": "Dendrobium"
            },
            {
                "species_id": "ficus_benjamina",
                "scientific_name": "Ficus benjamina",
                "common_name": "Weeping Fig",
                "family": "Moraceae",
                "genus": "Ficus"
            },
            {
                "species_id": "hibiscus_rosa_sinensis",
                "scientific_name": "Hibiscus rosa-sinensis",
                "common_name": "Chinese Hibiscus",
                "family": "Malvaceae",
                "genus": "Hibiscus"
            },
            {
                "species_id": "plumeria_rubra",
                "scientific_name": "Plumeria rubra",
                "common_name": "Frangipani",
                "family": "Apocynaceae",
                "genus": "Plumeria"
            },
            {
                "species_id": "bougainvillea_spectabilis",
                "scientific_name": "Bougainvillea spectabilis",
                "common_name": "Great Bougainvillea",
                "family": "Nyctaginaceae",
                "genus": "Bougainvillea"
            }
        ]
    
    def predict(self, image_data: bytes) -> List[IdentificationResult]:
        """Mock prediction - returns random species with confidence scores"""
        import random
        
        # Simulate processing time
        time.sleep(0.1)
        
        # Generate mock results
        results = []
        selected_species = random.sample(self.mock_species, min(3, len(self.mock_species)))
        
        for i, species in enumerate(selected_species):
            confidence = random.uniform(0.6, 0.95) if i == 0 else random.uniform(0.3, 0.7)
            results.append(IdentificationResult(
                species_id=species["species_id"],
                scientific_name=species["scientific_name"],
                common_name=species["common_name"],
                confidence=round(confidence, 3),
                family=species["family"],
                genus=species["genus"]
            ))
        
        # Sort by confidence
        results.sort(key=lambda x: x.confidence, reverse=True)
        return results

# Initialize mock model
ml_model = MockMLModel()

def validate_image(file: UploadFile) -> tuple[bool, str]:
    """Validate uploaded image file"""
    # Check file size
    if file.size and file.size > settings.MAX_FILE_SIZE:
        return False, f"File size exceeds maximum limit of {settings.MAX_FILE_SIZE / (1024*1024):.1f}MB"
    
    # Check content type
    if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
        return False, f"Unsupported file type. Allowed types: {', '.join(settings.ALLOWED_IMAGE_TYPES)}"
    
    return True, "Valid"

def process_image(image_data: bytes) -> dict:
    """Process and analyze image"""
    try:
        image = Image.open(io.BytesIO(image_data))
        return {
            "width": image.width,
            "height": image.height,
            "format": image.format,
            "mode": image.mode,
            "size_bytes": len(image_data)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image format: {str(e)}")

@router.post("/", response_model=IdentificationResponse)
async def identify_plant(
    request: Request,
    file: UploadFile = File(..., description="Plant image file (JPEG, PNG, WebP)")
):
    """Identify plant species from uploaded image"""
    start_time = time.time()
    request_id = str(uuid.uuid4())
    
    logger.info(f"Processing identification request {request_id}")
    
    # Validate image
    is_valid, validation_message = validate_image(file)
    if not is_valid:
        raise HTTPException(status_code=400, detail=validation_message)
    
    try:
        # Read image data
        image_data = await file.read()
        
        # Process image
        image_info = process_image(image_data)
        
        # Run ML prediction
        results = ml_model.predict(image_data)
        
        # Filter results by confidence threshold
        filtered_results = [
            result for result in results 
            if result.confidence >= settings.CONFIDENCE_THRESHOLD
        ]
        
        processing_time = time.time() - start_time
        
        # Get user info from request state (set by auth middleware)
        user_info = getattr(request.state, 'user', {})
        
        response = IdentificationResponse(
            request_id=request_id,
            timestamp=time.time(),
            results=filtered_results,
            processing_time=round(processing_time, 4),
            image_info=image_info,
            metadata={
                "user_id": user_info.get("user_id"),
                "tier": user_info.get("tier"),
                "confidence_threshold": settings.CONFIDENCE_THRESHOLD,
                "total_candidates": len(results),
                "filtered_candidates": len(filtered_results)
            }
        )
        
        logger.info(f"Identification completed for request {request_id} in {processing_time:.4f}s")
        return response
        
    except Exception as e:
        logger.error(f"Error processing identification request {request_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )

@router.get("/status")
async def get_identification_status():
    """Get identification service status"""
    return {
        "service": "Plant Identification",
        "status": "operational",
        "model_version": "mock-v1.0",
        "supported_formats": settings.ALLOWED_IMAGE_TYPES,
        "max_file_size_mb": settings.MAX_FILE_SIZE / (1024*1024),
        "confidence_threshold": settings.CONFIDENCE_THRESHOLD,
        "timestamp": time.time()
    }