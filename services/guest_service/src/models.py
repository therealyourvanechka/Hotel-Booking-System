from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Guest(Base):
    __tablename__ = "guests"

    passport = Column(String, primary_key=True)  # уникальный идентификатор
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    def __repr__(self):
        return f"<Guest(passport='{self.passport}', full_name='{self.full_name}', phone='{self.phone}')>"
