from pydantic import BaseModel
from typing import Optional

class GuestBase(BaseModel):
    full_name: str
    phone: str

class GuestCreate(GuestBase):
    passport: str

class GuestResponse(GuestBase):
    passport: str

    model_config = {
        "from_attributes": True
    }
