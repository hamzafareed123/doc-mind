from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from src.core.config import settings

engine = create_engine(settings.DATABASE_URL,echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def create_tables():
    from src.db.model import ChatHistory 
    print("Table Creating")
    Base.metadata.create_all(bind=engine) 
    print("Created Table")