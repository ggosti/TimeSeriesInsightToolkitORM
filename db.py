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

# Create a DBSession instance
#DBSession = sessionmaker(bind=engine)
session = SessionLocal() #DBSession()

init_db()

# Clear existing data from tables
#session.query(RawEvent).delete()
#session.query(RawGroup).delete()
#session.query(RawRecord).delete()
#session.commit()#

