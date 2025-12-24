from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    passport = Column(String, nullable=False) # Внешний ключ логически, но не физически
    room_number = Column(Integer, nullable=False) # Внешний ключ логически
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    status = Column(String, default="reserved")  # reserved, checked_in, checked_out, cancelled

    def __repr__(self):
        return f"<Booking(id={self.id}, passport='{self.passport}', room={self.room_number}, status='{self.status}')>"
