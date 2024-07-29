from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "sqlite:///data/data.db"

# Create engine
engine = create_engine(DATABASE_URL)

# Create a Session class to handle DB sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)