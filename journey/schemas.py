# schemas.py
from pydantic import BaseModel
from typing import List, Optional
import uuid


class ActivityBase(BaseModel):
    id: Optional[uuid.UUID] = None
    status: str


class ActivityCreate(ActivityBase):
    pass


class Activity(ActivityBase):
    id: uuid.UUID

    class Config:
        orm_mode = True


class JourneyBase(BaseModel):
    theme: str
    description: Optional[str] = None


class JourneyCreate(JourneyBase):
    activities: List[ActivityCreate] = []


class Journey(JourneyBase):
    uuid: uuid.UUID
    activities: List[Activity] = []

    class Config:
        orm_mode = True
