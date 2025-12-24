from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship
from .db import Base

# Таблица гостей
class Guest(Base):
    __tablename__ = "guests"

    passport = Column(String, primary_key=True)  # уникальный идентификатор
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    # связь с бронированиями
    bookings = relationship("Booking", back_populates="guest")

    def __repr__(self):
        return f"<Guest(passport='{self.passport}', full_name='{self.full_name}', phone='{self.phone}')>"

# Таблица номеров
class Room(Base):
    __tablename__ = "rooms"

    room_number = Column(Integer, primary_key=True)  # уникальный номер комнаты
    room_type = Column(String, nullable=False)       # например, стандарт, люкс
    price = Column(Float, nullable=False)            # цена за ночь

    # связь с бронированиями
    bookings = relationship("Booking", back_populates="room")


# Таблица бронирований
class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    passport = Column(String, ForeignKey("guests.passport"), nullable=False)
    room_number = Column(Integer, ForeignKey("rooms.room_number"), nullable=False)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    status = Column(String, default="reserved")  # reserved, checked_in, checked_out, cancelled

    # связи
    guest = relationship("Guest", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")


    def __repr__(self):
        return f"<Booking(id={self.id}, passport='{self.passport}', room={self.room_number}, status='{self.status}')>"
