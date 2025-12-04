from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import crud, schemas
from database import get_db
from supabase_client import upload_image_to_supabase

router = APIRouter(tags=["Teams"])

@router.get("/teams", response_model=List[schemas.Team])
def api_get_teams(q: Optional[str] = "", skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_teams(db, q=q, skip=skip, limit=limit)

@router.get("/teams/{team_id}", response_model=schemas.Team)
def api_get_team(team_id: int, db: Session = Depends(get_db)):
    t = crud.get_team(db, team_id)
    if not t:
        raise HTTPException(status_code=404, detail="Team not found")
    return t

@router.post("/teams", response_model=schemas.Team)
async def api_create_team(
    name: str = Form(...),
    founded_date: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    image_filename = None
    image_url = None
    if image:
        content = await image.read()
        safe_name = f"teams/{name.replace(' ','_')}_{image.filename}"
        image_url = upload_image_to_supabase(content, safe_name, content_type=image.content_type)
        image_filename = image.filename

    team_schema = schemas.TeamCreate(name=name, founded_date=None, description=description, active=True)
    return crud.create_team(db, team_schema, image_filename=image_filename, image_url=image_url)

@router.put("/teams/{team_id}", response_model=schemas.Team)
def api_update_team(team_id: int, team: schemas.TeamCreate, db: Session = Depends(get_db)):
    updated = crud.update_team(db, team_id, team)
    if not updated:
        raise HTTPException(status_code=404, detail="Team not found")
    return updated

@router.delete("/teams/{team_id}")
def api_delete_team(team_id: int, db: Session = Depends(get_db)):
    deleted = crud.soft_delete_team(db, team_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Team not found")
    return {"message": "Team soft-deleted"}

@router.put("/teams/{team_id}/restore")
def api_restore_team(team_id: int, db: Session = Depends(get_db)):
    restored = crud.restore_team(db, team_id)
    if not restored:
        raise HTTPException(status_code=404, detail="Team not found")
    return {"message": "Team restored"}