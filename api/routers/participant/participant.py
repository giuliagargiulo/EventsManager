from typing import List
import uuid
from fastapi import APIRouter, Depends
from api.database import get_db
from databases import Database
from pydantic import BaseModel, Field, EmailStr

router = APIRouter(prefix="/participants", tags=["participants"])


class Participant(BaseModel):
    name: str = Field(...,
                      description="Name of the participant",
                      example="Giulia")
    surname: str = Field(..., 
                         description="Surname of the participant",
                         example="Gargiulo")
    email: EmailStr = Field(...,
                            description="Email of the participant",
                            example="giulia.gargiulo@example.com")
    phone: str = Field(...,
                       description="Phone number of the participant",
                       example="+123456789",
                       max_length=15)
    
class ParticipantBrief(BaseModel):
    uu_id: uuid.UUID = Field(..., 
                       description="UUID version 7 of the participant",
                       example="123e4567-e89b-12d3-a456-426614174000")
    name: str = Field(...,
                      description="Name of the participant",
                      example="Giulia")

class ParticipantOut(Participant):
    uu_id: uuid.UUID = Field(..., 
                       description="UUID version 7 of the participant",
                       example="123e4567-e89b-12d3-a456-426614174000")

# CRUD Operations for Participants
# CREATE

@router.post("/",
             summary="Create a Participant",
             description="Create a new participant in the database",
             response_description="A message indicating the result of the creation operation")
async def create_participant(participant: Participant, db: Database = Depends(get_db)):
    query = ("INSERT INTO tbl_participant (name, surname, email, phone) "
             "VALUES (:name, :surname, :email, :phone) "
             "RETURNING uu_id;")
    q_data = participant.dict()
    row = await db.fetch_one(query, q_data)
    return {"message": "Participant created successfully", "id": row['uu_id']}

# READ


@router.get("/",
            summary="Get All Participants",
            description="Retrieve all participants from the database",
            response_description="A list of participants in JSON format",
            response_model=List[ParticipantBrief])
async def get_participants(db: Database= Depends(get_db)):
    query= ("SELECT uu_id, name "
            "FROM tbl_participant;")
    records = await db.fetch_all(query)
    return [dict(record) for record in records]


@router.get("/{participant_id}",
            summary="Get Participant by ID",
            description="Retrieve a specific participant by its ID from the database",
            response_description="A participant in JSON format",
            response_model=ParticipantOut)
async def get_participant(participant_id: str, db: Database = Depends(get_db)):
    query= ("SELECT name, surname, email, phone, uu_id "
            "FROM tbl_participant "
            "WHERE uu_id = :uu_id;")
    q_data = {"uu_id": participant_id}
    participant = await db.fetch_one(query, q_data)
    if not participant:
        return {"Error": "Participant not found"}
    return dict(participant)

# UPDATE


@router.put("/{participant_id}",
            summary="Update a Participant",
            description="Update an existing participant in the database",
            response_description="A message indicating the result of the update operation")
async def update_participant(participant_id: str, participant: Participant, db: Database = Depends(get_db)):
    query = ("SELECT uu_id "
             "FROM tbl_participant "
             "WHERE uu_id = :uu_id;")
    q_data = {"uu_id": participant_id}
    db_participant = await db.fetch_one(query, q_data)
    if not db_participant:
        return {"Error": "Participant not found"}
    query = ("UPDATE tbl_participant "
             "SET name = :name, "
                "    surname = :surname, "
                "    email = :email, "
                "    phone = :phone "
                "WHERE uu_id = :uu_id;")
    q_data = {
        "name": participant.name,
        "surname": participant.surname,
        "email": participant.email,
        "phone": participant.phone,
        "uu_id": participant_id
    }
    await db.execute(query, q_data)
    return {"message": "Participant updated successfully"}

# DELETE


@router.delete("/{participant_id}",
               summary="Delete a Participant",
               description="Delete a participant from the database",
               response_description="A message indicating the result of the deletion operation")
async def delete_participant(participant_id: str, db: Database = Depends(get_db)):
    query = ("SELECT uu_id "
             "FROM tbl_participant "
             "WHERE uu_id = :uu_id;")
    q_data = {"uu_id": participant_id}
    db_participant = await db.fetch_one(query, q_data)
    if not db_participant:
        return {"Error": "Participant not found"}
    query = ("DELETE FROM tbl_participant "
             "WHERE uu_id = :uu_id;")
    await db.execute(query, q_data)
    return {"message": "Participant deleted successfully"}
