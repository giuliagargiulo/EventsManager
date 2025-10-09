from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api import classes
from api import models
from api.database import get_db

router = APIRouter(prefix="/participants", tags=["participants"])

# CRUD Operations for Participants
# CREATE

@router.post("/")
def create_participant(participant: classes.Participant, db: Session = Depends(get_db)):
    db_participant = models.Participant(
        name=participant.name,
        surname=participant.surname,
        email=participant.email,
        phone=participant.phone
    )
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)
    return db_participant

# READ
@router.get("/")
def get_participants(db: Session = Depends(get_db)):
    return db.query(models.Participant).all()

@router.get("/{participant_id}")
def get_participant(participant_id: int, db: Session = Depends(get_db)):
    db_participant = db.query(models.Participant).filter(models.Participant.id == participant_id).first()
    if db_participant is None:
        return {"error": "Participant not found"}
    return db_participant

# UPDATE
@router.put("/{participant_id}")
def update_participant(participant_id: int, updated_participant: classes.Participant, db: Session = Depends(get_db)):
    db_participant = db.query(models.Participant).filter(models.Participant.id == participant_id).first()
    if db_participant is None:
        return {"error": "Participant not found"}
    db_participant.name = updated_participant.name
    db_participant.surname = updated_participant.surname
    db_participant.email = updated_participant.email
    db_participant.phone = updated_participant.phone
    db.commit()
    db.refresh(db_participant)
    return db_participant

# DELETE
@router.delete("/{participant_id}")
def delete_participant(participant_id: int, db: Session = Depends(get_db)):
    db_participant = db.query(models.Participant).filter(models.Participant.id == participant_id).first()
    if db_participant is None:
        return {"error": "Participant not found"}
    db.delete(db_participant)
    db.commit()
    return {"message": "Participant deleted successfully"}