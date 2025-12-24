# app/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import DATABASE_URL
except ImportError:
    from example_config import DATABASE_URL
    print("Используется example_config.py! Создайте config.py с реальными настройками")

class EngineSingleton:
    _instance = None

    @staticmethod
    def get_instance(database_url):
        if EngineSingleton._instance is None:
            EngineSingleton._instance = create_engine(database_url)
        return EngineSingleton._instance


engine = EngineSingleton.get_instance(DATABASE_URL)


SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def init_db():
    from app import models  # Импорт моделей для создания таблиц
    Base.metadata.create_all(bind=engine)