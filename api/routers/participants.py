from fastapi import APIRouter, Depends
from api import classes
from api.database import get_db
from asyncpg import Connection


router = APIRouter(prefix="/participants", tags=["participants"])

# CRUD Operations for Participants
# CREATE

@router.post("/")
async def create_participant(participant: classes.Participant, db: Connection = Depends(get_db)):
    query = "INSERT INTO participants (first_name, last_name, email, phone) VALUES ($1, $2, $3, $4) RETURNING id;"
    row = await db.fetchrow(query, participant.first_name, participant.last_name, participant.email, participant.phone)
    return {"message": "Participant created successfully", "id": row['id']}
    
# READ
@router.get("/")
async def get_participants(db: Connection = Depends(get_db)):
    return await db.fetch("SELECT * FROM participants;")

@router.get("/{participant_id}")
async def get_participant(participant_id: int, db: Connection = Depends(get_db)):
    participant = await db.fetchrow("SELECT * FROM participants WHERE id = $1", participant_id)
    if not participant:
        return {"Error": "Participant not found"}
    return participant

# UPDATE
@router.put("/{participant_id}")
async def update_participant(participant_id: int, updated_participant: classes.Participant, db: Connection = Depends(get_db)):
    query = """
        UPDATE participants SET first_name = $1, last_name = $2, email = $3, phone = $4 WHERE id = $5
    """
    values = (updated_participant.first_name, updated_participant.last_name, updated_participant.email, updated_participant.phone, participant_id)
    row = await db.fetchrow(query, *values)
    print({"message": "Participant updated successfully"})
    return dict(row)

# DELETE
@router.delete("/{participant_id}")
async def delete_participant(participant_id: int, db: Connection = Depends(get_db)):
    query = "DELETE FROM participants WHERE id = $1"
    await db.execute(query, (participant_id,))
    return {"message": "Participant deleted successfully"}