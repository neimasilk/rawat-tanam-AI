from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import time
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Response models
class SpeciesInfo(BaseModel):
    species_id: str
    scientific_name: str
    common_name: str
    local_names: List[str]
    family: str
    genus: str
    description: str
    habitat: str
    distribution: List[str]
    conservation_status: str
    uses: List[str]
    characteristics: dict
    images: List[str]

class SpeciesListResponse(BaseModel):
    species: List[SpeciesInfo]
    total: int
    page: int
    per_page: int
    total_pages: int

class SpeciesSearchResponse(BaseModel):
    results: List[SpeciesInfo]
    query: str
    total_results: int
    search_time: float

# Mock species database
class MockSpeciesDatabase:
    def __init__(self):
        self.species_data = [
            {
                "species_id": "dendrobium_nobile",
                "scientific_name": "Dendrobium nobile",
                "common_name": "Noble Dendrobium",
                "local_names": ["Anggrek Dendrobium", "Anggrek Mulia"],
                "family": "Orchidaceae",
                "genus": "Dendrobium",
                "description": "Epiphytic orchid with pseudobulbs and fragrant flowers",
                "habitat": "Tropical forests, epiphytic on trees",
                "distribution": ["Sumatra", "Java", "Kalimantan", "Sulawesi"],
                "conservation_status": "Least Concern",
                "uses": ["Ornamental", "Traditional medicine"],
                "characteristics": {
                    "height": "30-60 cm",
                    "flower_color": "White, pink, purple",
                    "blooming_season": "Dry season",
                    "growth_habit": "Epiphytic"
                },
                "images": ["dendrobium_nobile_1.jpg", "dendrobium_nobile_2.jpg"]
            },
            {
                "species_id": "ficus_benjamina",
                "scientific_name": "Ficus benjamina",
                "common_name": "Weeping Fig",
                "local_names": ["Beringin Kecil", "Pohon Karet Hias"],
                "family": "Moraceae",
                "genus": "Ficus",
                "description": "Small to medium-sized tree with glossy leaves",
                "habitat": "Tropical and subtropical regions",
                "distribution": ["Java", "Sumatra", "Bali", "Nusa Tenggara"],
                "conservation_status": "Least Concern",
                "uses": ["Ornamental", "Indoor plant", "Bonsai"],
                "characteristics": {
                    "height": "2-10 m",
                    "leaf_shape": "Oval, glossy",
                    "growth_habit": "Tree/shrub",
                    "light_requirement": "Bright indirect light"
                },
                "images": ["ficus_benjamina_1.jpg", "ficus_benjamina_2.jpg"]
            },
            {
                "species_id": "hibiscus_rosa_sinensis",
                "scientific_name": "Hibiscus rosa-sinensis",
                "common_name": "Chinese Hibiscus",
                "local_names": ["Kembang Sepatu", "Bunga Raya"],
                "family": "Malvaceae",
                "genus": "Hibiscus",
                "description": "Flowering shrub with large, colorful flowers",
                "habitat": "Tropical gardens and landscapes",
                "distribution": ["Throughout Indonesia"],
                "conservation_status": "Least Concern",
                "uses": ["Ornamental", "Traditional medicine", "Hair care"],
                "characteristics": {
                    "height": "1-4 m",
                    "flower_color": "Red, pink, yellow, white, orange",
                    "flower_size": "8-15 cm diameter",
                    "blooming_season": "Year-round"
                },
                "images": ["hibiscus_rosa_sinensis_1.jpg", "hibiscus_rosa_sinensis_2.jpg"]
            },
            {
                "species_id": "plumeria_rubra",
                "scientific_name": "Plumeria rubra",
                "common_name": "Frangipani",
                "local_names": ["Kamboja", "Bunga Kamboja"],
                "family": "Apocynaceae",
                "genus": "Plumeria",
                "description": "Deciduous tree with fragrant, waxy flowers",
                "habitat": "Tropical and subtropical regions",
                "distribution": ["Java", "Bali", "Sumatra", "Sulawesi"],
                "conservation_status": "Least Concern",
                "uses": ["Ornamental", "Religious ceremonies", "Perfume"],
                "characteristics": {
                    "height": "3-8 m",
                    "flower_color": "White, yellow, pink, red",
                    "fragrance": "Strong, sweet",
                    "leaf_type": "Deciduous"
                },
                "images": ["plumeria_rubra_1.jpg", "plumeria_rubra_2.jpg"]
            },
            {
                "species_id": "bougainvillea_spectabilis",
                "scientific_name": "Bougainvillea spectabilis",
                "common_name": "Great Bougainvillea",
                "local_names": ["Bunga Kertas", "Bugenvil"],
                "family": "Nyctaginaceae",
                "genus": "Bougainvillea",
                "description": "Thorny ornamental vine with colorful bracts",
                "habitat": "Tropical and subtropical gardens",
                "distribution": ["Throughout Indonesia"],
                "conservation_status": "Least Concern",
                "uses": ["Ornamental", "Hedge plant", "Traditional medicine"],
                "characteristics": {
                    "height": "1-12 m (climbing)",
                    "bract_color": "Purple, pink, red, orange, white",
                    "growth_habit": "Climbing vine",
                    "thorns": "Present"
                },
                "images": ["bougainvillea_spectabilis_1.jpg", "bougainvillea_spectabilis_2.jpg"]
            }
        ]
    
    def get_species_by_id(self, species_id: str) -> Optional[dict]:
        """Get species by ID"""
        for species in self.species_data:
            if species["species_id"] == species_id:
                return species
        return None
    
    def search_species(self, query: str, limit: int = 10) -> List[dict]:
        """Search species by name or characteristics"""
        query_lower = query.lower()
        results = []
        
        for species in self.species_data:
            # Search in scientific name, common name, and local names
            if (query_lower in species["scientific_name"].lower() or
                query_lower in species["common_name"].lower() or
                any(query_lower in name.lower() for name in species["local_names"]) or
                query_lower in species["family"].lower() or
                query_lower in species["genus"].lower()):
                results.append(species)
        
        return results[:limit]
    
    def get_species_list(self, page: int = 1, per_page: int = 10, family: str = None) -> tuple[List[dict], int]:
        """Get paginated species list with optional family filter"""
        filtered_data = self.species_data
        
        if family:
            filtered_data = [s for s in self.species_data if s["family"].lower() == family.lower()]
        
        total = len(filtered_data)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        return filtered_data[start_idx:end_idx], total

# Initialize mock database
species_db = MockSpeciesDatabase()

@router.get("/stats")
async def get_database_stats():
    """Get database statistics"""
    total_species = len(species_db.species_data)
    families = set(species["family"] for species in species_db.species_data)
    genera = set(species["genus"] for species in species_db.species_data)
    
    conservation_status = {}
    for species in species_db.species_data:
        status = species["conservation_status"]
        conservation_status[status] = conservation_status.get(status, 0) + 1
    
    return {
        "total_species": total_species,
        "total_families": len(families),
        "total_genera": len(genera),
        "conservation_status_distribution": conservation_status,
        "database_version": "mock-v1.0",
        "last_updated": time.time()
    }

@router.get("/{species_id}", response_model=SpeciesInfo)
async def get_species(species_id: str):
    """Get detailed information about a specific species"""
    species_data = species_db.get_species_by_id(species_id)
    
    if not species_data:
        raise HTTPException(
            status_code=404,
            detail=f"Species with ID '{species_id}' not found"
        )
    
    return SpeciesInfo(**species_data)

@router.get("/", response_model=SpeciesListResponse)
async def list_species(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    family: Optional[str] = Query(None, description="Filter by plant family")
):
    """Get paginated list of species"""
    species_list, total = species_db.get_species_list(page, per_page, family)
    total_pages = (total + per_page - 1) // per_page
    
    species_objects = [SpeciesInfo(**species) for species in species_list]
    
    return SpeciesListResponse(
        species=species_objects,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )

@router.get("/search/", response_model=SpeciesSearchResponse)
async def search_species(
    q: str = Query(..., min_length=2, description="Search query"),
    limit: int = Query(10, ge=1, le=50, description="Maximum results")
):
    """Search species by name or characteristics"""
    start_time = time.time()
    
    results = species_db.search_species(q, limit)
    search_time = time.time() - start_time
    
    species_objects = [SpeciesInfo(**species) for species in results]
    
    return SpeciesSearchResponse(
        results=species_objects,
        query=q,
        total_results=len(results),
        search_time=round(search_time, 4)
    )

@router.get("/families/list")
async def list_families():
    """Get list of all plant families in the database"""
    families = list(set(species["family"] for species in species_db.species_data))
    families.sort()
    
    family_counts = {}
    for family in families:
        count = len([s for s in species_db.species_data if s["family"] == family])
        family_counts[family] = count
    
    return {
        "families": families,
        "family_counts": family_counts,
        "total_families": len(families),
        "total_species": len(species_db.species_data)
    }