# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid

class ProfileCreate(BaseModel):
    name: str
    country: Optional[str] = None
    email: EmailStr

class ProfileResponse(ProfileCreate):
    uuid: uuid.UUID

    class Config:
        orm_mode = True
