import httpx
import asyncio
from typing import Dict, List, Optional, Any
import logging
import time
from config import settings

logger = logging.getLogger(__name__)

class TanamRawatClient:
    """Client for integrating with Tanam Rawat software backend"""
    
    def __init__(self, base_url: str = None, api_key: str = None):
        self.base_url = base_url or settings.TANAM_RAWAT_API_URL
        self.api_key = api_key or settings.TANAM_RAWAT_API_KEY
        self.timeout = 30.0
        self.max_retries = 3
        self.retry_delay = 1.0
        
        # HTTP client configuration
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            headers={
                "User-Agent": "Rawat-Tanam-AI-Integration/1.0",
                "Content-Type": "application/json"
            }
        )
        
        if self.api_key:
            self.client.headers["Authorization"] = f"Bearer {self.api_key}"
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Dict = None, 
        params: Dict = None,
        files: Dict = None
    ) -> Dict[str, Any]:
        """Make HTTP request with retry logic"""
        url = f"{endpoint}"
        
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Making {method} request to {url} (attempt {attempt + 1})")
                
                if method.upper() == "GET":
                    response = await self.client.get(url, params=params)
                elif method.upper() == "POST":
                    if files:
                        response = await self.client.post(url, data=data, files=files)
                    else:
                        response = await self.client.post(url, json=data, params=params)
                elif method.upper() == "PUT":
                    response = await self.client.put(url, json=data, params=params)
                elif method.upper() == "DELETE":
                    response = await self.client.delete(url, params=params)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                # Check if request was successful
                response.raise_for_status()
                
                # Parse JSON response
                result = response.json()
                logger.info(f"Request successful: {method} {url}")
                return result
                
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
                if e.response.status_code < 500 or attempt == self.max_retries - 1:
                    raise
                
            except httpx.RequestError as e:
                logger.error(f"Request error: {str(e)}")
                if attempt == self.max_retries - 1:
                    raise
            
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                if attempt == self.max_retries - 1:
                    raise
            
            # Wait before retry
            if attempt < self.max_retries - 1:
                await asyncio.sleep(self.retry_delay * (2 ** attempt))
        
        raise Exception(f"Failed to complete request after {self.max_retries} attempts")
    
    async def health_check(self) -> Dict[str, Any]:
        """Check if Tanam Rawat backend is healthy"""
        try:
            result = await self._make_request("GET", "/health")
            return {
                "status": "healthy",
                "tanam_rawat_response": result,
                "timestamp": time.time()
            }
        except Exception as e:
            logger.error(f"Tanam Rawat health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": time.time()
            }
    
    async def get_plant_data(self, plant_id: str) -> Optional[Dict[str, Any]]:
        """Get plant data from Tanam Rawat"""
        try:
            result = await self._make_request("GET", f"/plants/{plant_id}")
            return self._transform_plant_data(result)
        except Exception as e:
            logger.error(f"Failed to get plant data for {plant_id}: {str(e)}")
            return None
    
    async def search_plants(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search plants in Tanam Rawat database"""
        try:
            params = {"q": query, "limit": limit}
            result = await self._make_request("GET", "/plants/search", params=params)
            
            plants = result.get("plants", [])
            return [self._transform_plant_data(plant) for plant in plants]
        except Exception as e:
            logger.error(f"Failed to search plants with query '{query}': {str(e)}")
            return []
    
    async def submit_identification(self, identification_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Submit identification result to Tanam Rawat"""
        try:
            # Transform our identification format to Tanam Rawat format
            tanam_rawat_data = self._transform_identification_data(identification_data)
            
            result = await self._make_request("POST", "/identifications", data=tanam_rawat_data)
            return result
        except Exception as e:
            logger.error(f"Failed to submit identification: {str(e)}")
            return None
    
    async def get_care_instructions(self, species_id: str) -> Optional[Dict[str, Any]]:
        """Get care instructions for a species from Tanam Rawat"""
        try:
            result = await self._make_request("GET", f"/care-instructions/{species_id}")
            return self._transform_care_instructions(result)
        except Exception as e:
            logger.error(f"Failed to get care instructions for {species_id}: {str(e)}")
            return None
    
    async def sync_species_data(self, species_list: List[str]) -> Dict[str, Any]:
        """Sync species data with Tanam Rawat"""
        try:
            data = {"species_ids": species_list}
            result = await self._make_request("POST", "/sync/species", data=data)
            return result
        except Exception as e:
            logger.error(f"Failed to sync species data: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def _transform_plant_data(self, tanam_rawat_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform Tanam Rawat plant data to our format"""
        return {
            "species_id": tanam_rawat_data.get("id"),
            "scientific_name": tanam_rawat_data.get("scientific_name"),
            "common_name": tanam_rawat_data.get("common_name"),
            "local_names": tanam_rawat_data.get("local_names", []),
            "family": tanam_rawat_data.get("family"),
            "genus": tanam_rawat_data.get("genus"),
            "description": tanam_rawat_data.get("description"),
            "care_level": tanam_rawat_data.get("care_difficulty"),
            "light_requirement": tanam_rawat_data.get("light_needs"),
            "water_requirement": tanam_rawat_data.get("water_needs"),
            "soil_type": tanam_rawat_data.get("soil_preference"),
            "temperature_range": tanam_rawat_data.get("temperature_range"),
            "humidity_preference": tanam_rawat_data.get("humidity_needs"),
            "fertilizer_needs": tanam_rawat_data.get("fertilizer_schedule"),
            "common_problems": tanam_rawat_data.get("common_issues", []),
            "propagation_methods": tanam_rawat_data.get("propagation", []),
            "source": "tanam_rawat",
            "last_updated": time.time()
        }
    
    def _transform_identification_data(self, our_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform our identification data to Tanam Rawat format"""
        return {
            "request_id": our_data.get("request_id"),
            "species_predictions": [
                {
                    "species_id": result.get("species_id"),
                    "confidence": result.get("confidence"),
                    "scientific_name": result.get("scientific_name")
                }
                for result in our_data.get("results", [])
            ],
            "image_metadata": our_data.get("image_info"),
            "processing_time": our_data.get("processing_time"),
            "timestamp": our_data.get("timestamp"),
            "source": "rawat_tanam_ai"
        }
    
    def _transform_care_instructions(self, tanam_rawat_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform Tanam Rawat care instructions to our format"""
        return {
            "species_id": tanam_rawat_data.get("species_id"),
            "care_instructions": {
                "watering": {
                    "frequency": tanam_rawat_data.get("watering_frequency"),
                    "amount": tanam_rawat_data.get("watering_amount"),
                    "tips": tanam_rawat_data.get("watering_tips", [])
                },
                "lighting": {
                    "type": tanam_rawat_data.get("light_type"),
                    "duration": tanam_rawat_data.get("light_duration"),
                    "intensity": tanam_rawat_data.get("light_intensity")
                },
                "fertilizing": {
                    "schedule": tanam_rawat_data.get("fertilizer_schedule"),
                    "type": tanam_rawat_data.get("fertilizer_type"),
                    "application": tanam_rawat_data.get("fertilizer_application")
                },
                "pruning": {
                    "frequency": tanam_rawat_data.get("pruning_frequency"),
                    "method": tanam_rawat_data.get("pruning_method"),
                    "timing": tanam_rawat_data.get("pruning_timing")
                },
                "repotting": {
                    "frequency": tanam_rawat_data.get("repotting_frequency"),
                    "soil_mix": tanam_rawat_data.get("soil_recommendation"),
                    "pot_size": tanam_rawat_data.get("pot_size_guide")
                }
            },
            "seasonal_care": tanam_rawat_data.get("seasonal_variations", {}),
            "troubleshooting": tanam_rawat_data.get("common_problems", []),
            "source": "tanam_rawat",
            "last_updated": time.time()
        }

# Singleton instance for global use
_tanam_rawat_client = None

async def get_tanam_rawat_client() -> TanamRawatClient:
    """Get singleton Tanam Rawat client instance"""
    global _tanam_rawat_client
    if _tanam_rawat_client is None:
        _tanam_rawat_client = TanamRawatClient()
    return _tanam_rawat_client

async def test_integration() -> Dict[str, Any]:
    """Test integration with Tanam Rawat backend"""
    async with TanamRawatClient() as client:
        # Test health check
        health = await client.health_check()
        
        # Test search functionality
        search_results = await client.search_plants("ficus", limit=5)
        
        return {
            "health_check": health,
            "search_test": {
                "query": "ficus",
                "results_count": len(search_results),
                "sample_results": search_results[:2] if search_results else []
            },
            "integration_status": "success" if health["status"] == "healthy" else "failed"
        }