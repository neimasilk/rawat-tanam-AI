from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from datetime import datetime
from config import settings
import logging

logger = logging.getLogger(__name__)

# Database setup
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class Species(Base):
    __tablename__ = "species"
    
    id = Column(Integer, primary_key=True, index=True)
    scientific_name = Column(String(255), unique=True, index=True, nullable=False)
    common_name = Column(String(255), index=True)
    family = Column(String(100), index=True)
    genus = Column(String(100), index=True)
    species_name = Column(String(100))
    description = Column(Text)
    habitat = Column(Text)
    distribution = Column(Text)
    conservation_status = Column(String(50))
    image_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    identifications = relationship("Identification", back_populates="species")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    tier = Column(String(20), default="free")  # free, professional, enterprise, partner
    api_key = Column(String(255), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    identifications = relationship("Identification", back_populates="user")

class Identification(Base):
    __tablename__ = "identifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    species_id = Column(Integer, ForeignKey("species.id"), nullable=True)
    image_path = Column(String(500), nullable=False)
    confidence_score = Column(Float, nullable=False)
    prediction_data = Column(Text)  # JSON string with full prediction results
    processing_time = Column(Float)  # Time taken for identification in seconds
    status = Column(String(20), default="completed")  # pending, processing, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="identifications")
    species = relationship("Species", back_populates="identifications")

class APIUsage(Base):
    __tablename__ = "api_usage"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    api_key = Column(String(255), index=True)
    endpoint = Column(String(255), nullable=False)
    method = Column(String(10), nullable=False)
    status_code = Column(Integer, nullable=False)
    response_time = Column(Float)  # Response time in milliseconds
    user_agent = Column(String(500))
    ip_address = Column(String(45))
    created_at = Column(DateTime, default=datetime.utcnow)

# Database dependency
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database initialization
def create_tables():
    """Create all database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

def init_db():
    """Initialize database with sample data"""
    create_tables()
    
    # Add sample species data
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Species).count() == 0:
            sample_species = [
                Species(
                    scientific_name="Ficus benjamina",
                    common_name="Weeping Fig",
                    family="Moraceae",
                    genus="Ficus",
                    species_name="benjamina",
                    description="A popular ornamental tree native to Asia and Australia",
                    habitat="Tropical and subtropical regions",
                    distribution="Native to Asia and Australia, widely cultivated",
                    conservation_status="Least Concern"
                ),
                Species(
                    scientific_name="Dendrobium nobile",
                    common_name="Noble Dendrobium",
                    family="Orchidaceae",
                    genus="Dendrobium",
                    species_name="nobile",
                    description="An epiphytic orchid native to Southeast Asia",
                    habitat="Epiphytic on trees in tropical forests",
                    distribution="Southeast Asia, Himalayas",
                    conservation_status="Near Threatened"
                ),
                Species(
                    scientific_name="Monstera deliciosa",
                    common_name="Swiss Cheese Plant",
                    family="Araceae",
                    genus="Monstera",
                    species_name="deliciosa",
                    description="A climbing plant known for its distinctive split leaves",
                    habitat="Tropical rainforests",
                    distribution="Central America, widely cultivated",
                    conservation_status="Least Concern"
                )
            ]
            
            for species in sample_species:
                db.add(species)
            
            db.commit()
            logger.info(f"Added {len(sample_species)} sample species to database")
        else:
            logger.info("Database already contains species data")
            
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_db()