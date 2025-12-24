# app/schemas.py
from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

# Guests
class GuestBase(BaseModel):
    full_name: str
    phone: str

class GuestCreate(GuestBase):
    passport_number: str  # паспорт обязателен при создании

class GuestResponse(GuestBase):
    passport_number: str

    model_config = {
        "from_attributes": True
    }

# Rooms
class RoomBase(BaseModel):
    room_type: Optional[str] = None
    price: float

class RoomCreate(RoomBase):
    room_number: str  # уникальный номер при создании

class RoomResponse(RoomBase):
    room_number: str

    model_config = {
        "from_attributes": True
    }

#  Bookings
class BookingBase(BaseModel):
    check_in: date
    check_out: date
    status: Optional[str] = "reserved"

class BookingCreate(BookingBase):
    guest_passport: str
    room_number: str

class BookingResponse(BookingBase):
    id: int
    guest_passport: str
    room_number: str

    model_config = {
        "from_attributes": True
    }
