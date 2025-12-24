from pydantic import BaseModel
from typing import Optional

class RoomBase(BaseModel):
    room_type: str
    price: float

class RoomCreate(RoomBase):
    room_number: int

class RoomResponse(RoomBase):
    room_number: int

    model_config = {
        "from_attributes": True
    }
