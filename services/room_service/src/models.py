from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Room(Base):
    __tablename__ = "rooms"

    room_number = Column(Integer, primary_key=True)  # уникальный номер комнаты
    room_type = Column(String, nullable=False)       # например, стандарт, люкс
    price = Column(Float, nullable=False)            # цена за ночь

    def __repr__(self):
        return f"<Room(room_number={self.room_number}, room_type='{self.room_type}', price={self.price})>"
