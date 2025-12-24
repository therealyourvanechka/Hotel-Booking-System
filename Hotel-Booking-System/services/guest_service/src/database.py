from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

import os

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./guest.db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

import time
from sqlalchemy.exc import OperationalError

def init_db():
    retries = 5
    while retries > 0:
        try:
            Base.metadata.create_all(bind=engine)
            print("Database connected and tables created.")
            return
        except OperationalError as e:
            retries -= 1
            print(f"Database connection failed. Retrying in 5 seconds... ({retries} retries left)")
            time.sleep(5)
    raise Exception("Could not connect to the database after several retries.")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
