# crud.py
from sqlalchemy.orm import Session
from . import models, schemas


def get_journey(db: Session, journey_uuid: str):
    return db.query(
        models.Journey).filter(models.Journey.uuid == journey_uuid).first()


def create_journey(db: Session, journey: schemas.JourneyCreate):
    db_journey = models.Journey(theme=journey.theme,
                                description=journey.description)
    db.add(db_journey)
    db.commit()
    db.refresh(db_journey)

    # Adicionar atividades, se houver
    for activity in journey.activities:
        db_activity = models.Activity(status=activity.status, journey_id=db_journey.uuid)
        db.add(db_activity)
    db.commit()

    db.refresh(db_journey)
    return db_journey


def update_journey(db: Session, journey_uuid: str,
                   journey: schemas.Journey):
    db_journey = db.query(
        models.Journey).filter(models.Journey.uuid == journey_uuid).first()
    if db_journey:
        db_journey.theme = journey.theme
        db_journey.description = journey.description
        db.query(models.Activity).filter(models.Activity.journey_id == journey_uuid).delete()

        for activity in journey.activities:
            db_activity = models.Activity(status=activity.status, journey_id=db_journey.uuid)
            db.add(db_activity)

        db.commit()
        db.refresh(db_journey)
    return db_journey


def delete_journey(db: Session, journey_uuid: str):
    db_journey = db.query(
        models.Journey).filter(models.Journey.uuid == journey_uuid).first()
    if db_journey:
        db.delete(db_journey)
        db.commit()
    return db_journey
