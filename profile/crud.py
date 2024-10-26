# crud.py
from sqlalchemy.orm import Session
from . import models, schemas


def get_profile(db: Session, profile_uuid: str):
    return db.query(
        models.Profile).filter(models.Profile.uuid == profile_uuid).first()


def create_profile(db: Session, profile: schemas.ProfileCreate):
    db_profile = models.Profile(name=profile.name,
                                country=profile.country,
                                email=profile.email)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def update_profile(db: Session, profile_uuid: str,
                   profile: schemas.ProfileCreate):
    db_profile = db.query(
        models.Profile).filter(models.Profile.uuid == profile_uuid).first()
    if db_profile:
        db_profile.name = profile.name
        db_profile.country = profile.country
        db_profile.email = profile.email
        db.commit()
        db.refresh(db_profile)
    return db_profile


def delete_profile(db: Session, profile_uuid: str):
    db_profile = db.query(
        models.Profile).filter(models.Profile.uuid == profile_uuid).first()
    if db_profile:
        db.delete(db_profile)
        db.commit()
    return db_profile
