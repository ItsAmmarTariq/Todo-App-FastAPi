from contextlib import contextmanager
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os

load_dotenv(".env")

sqlDatabaseUrl : str = os.getenv("SQLALCHEMY_DATABASE_URL")


engine = create_engine(sqlDatabaseUrl)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

print("Database URL:", sqlDatabaseUrl)