from pydantic import BaseModel
from datetime import date
from typing import Optional

class BookingBase(BaseModel):
    check_in: date
    check_out: date
    status: Optional[str] = "reserved"

class BookingCreate(BookingBase):
    guest_passport: str
    room_number: int # changed from str to int to match model
    guest_name: str # Added for automatic guest creation/check
    guest_phone: str # Added for automatic guest creation/check

class BookingResponse(BookingBase):
    id: int
    passport: str
    room_number: int

    model_config = {
        "from_attributes": True
    }
