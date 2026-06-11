from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from config import SQLALCHEMY_DATABASE_URL, SECRET_KEY, ALGORITHM

# from dotenv import load_dotenv
# import os
# load_dotenv()

Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency para ser usada no FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
