# models.py
from sqlalchemy import Column, String, UUID, Integer, ForeignKey
import uuid
from sqlalchemy.orm import relationship
from util.database import Base


# Modelo para o perfil
class Journey(Base):
    '''
    Profile
    '''
    __tablename__ = "journey"

    # id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    theme = Column(String, nullable=False)
    description = Column(String, nullable=True)
    activities = relationship("Activity", back_populates="journey", cascade="all, delete-orphan")


# Modelo para as atividades
class Activity(Base):
    '''
    Activity
    '''
    __tablename__ = "activities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    journey_id = Column(UUID, ForeignKey("journey.uuid", ondelete="CASCADE"), nullable=False)
    status = Column(String, nullable=False)
    profile = relationship("Journey", back_populates="activities")