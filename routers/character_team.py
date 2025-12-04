from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, schemas
from database import get_db

router = APIRouter(tags=["Character-Team"])

@router.post("/character_team", response_model=schemas.CharacterTeam)
def api_create_character_team(ct: schemas.CharacterTeamCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_character_team(db, ct)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/character_team", response_model=List[schemas.CharacterTeam])
def api_list_character_team(db: Session = Depends(get_db)):
    return crud.get_character_teams(db)

@router.delete("/character_team/{ct_id}")
def api_delete_character_team(ct_id: int, db: Session = Depends(get_db)):
    crud.delete_character_team(db, ct_id)
    return {"message": "Character-Team relationship deleted"}