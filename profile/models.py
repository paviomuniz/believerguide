# models.py
from sqlalchemy import Column, String, UUID
import uuid
from util.database import Base

class Profile(Base):
    __tablename__ = "profile"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    country = Column(String(100))
    email = Column(String(255), nullable=False, unique=True)