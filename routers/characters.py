from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import crud, schemas
from database import get_db
from supabase_client import upload_image_to_supabase
import os

router = APIRouter(tags=["Characters"])

@router.get("/characters", response_model=List[schemas.Character])
def api_get_characters(q: Optional[str] = "", skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_characters(db, q=q, skip=skip, limit=limit)

@router.get("/characters/{character_id}", response_model=schemas.Character)
def api_get_character(character_id: int, db: Session = Depends(get_db)):
    c = crud.get_character(db, character_id)
    if not c:
        raise HTTPException(status_code=404, detail="Character not found")
    return c
@router.post("/characters", response_model=schemas.Character)
async def api_create_character(
    name: str = Form(...),
    alias: str = Form(None),
    alignment: str = Form(...),
    description: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    image_url = None
    if image:
        content = await image.read()
        safe_name = f"{name.replace(' ','_')}_{image.filename}"
        try:
            image_url = upload_image_to_supabase(content, safe_name, content_type=image.content_type)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    char_schema = schemas.CharacterCreate(
        name=name, alias=alias, alignment=alignment, description=description, active=True
    )

    return crud.create_character(db, char_schema, image_url=image_url)

@router.put("/characters/{character_id}", response_model=schemas.Character)
def api_update_character(character_id: int, character: schemas.CharacterCreate, db: Session = Depends(get_db)):
    updated = crud.update_character(db, character_id, character)
    if not updated:
        raise HTTPException(status_code=404, detail="Character not found")
    return updated

@router.delete("/characters/{character_id}")
def api_delete_character(character_id: int, db: Session = Depends(get_db)):
    deleted = crud.soft_delete_character(db, character_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Character not found")
    return {"message": "Character soft-deleted"}

@router.put("/characters/{character_id}/restore")
def api_restore_character(character_id: int, db: Session = Depends(get_db)):
    restored = crud.restore_character(db, character_id)
    if not restored:
        raise HTTPException(status_code=404, detail="Character not found")
    return {"message": "Character restored"}
