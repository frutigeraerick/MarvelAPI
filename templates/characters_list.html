from fastapi import APIRouter, Request, Depends, UploadFile, File, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db
from supabase_client import upload_image_to_supabase

router = APIRouter(tags=["Web Pages"])

# Página de inicio
@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db), q: str = ""):
    characters = crud.get_characters(db, q=q)
    return request.app.state.templates.TemplateResponse("index.html", {
        "request": request,
        "characters": characters
    })

# Listar personajes
@router.get("/characters", response_class=HTMLResponse)
def characters_page(request: Request, db: Session = Depends(get_db), q: str = ""):
    characters = crud.get_characters(db, q=q)
    return request.app.state.templates.TemplateResponse(
        "characters_list.html",
        {"request": request, "characters": characters, "q": q}
    )

# Crear personaje (formulario)
@router.get("/characters/new", response_class=HTMLResponse)
def new_character_page(request: Request):
    return request.app.state.templates.TemplateResponse("characters_new.html", {"request": request})

# Crear personaje (POST)
@router.post("/characters/new")
async def create_character(
    request: Request,
    name: str = Form(...),
    alias: str = Form(None),
    alignment: str = Form(...),
    description: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    image_filename = None
    image_url = None
    if image:
        content = await image.read()
        safe_name = f"characters/{name.replace(' ', '_')}_{image.filename}"
        image_url = upload_image_to_supabase(content, safe_name, content_type=image.content_type)
        image_filename = image.filename

    character_data = schemas.CharacterCreate(
        name=name,
        alias=alias,
        alignment=alignment,
        description=description,
        active=True
    )
    crud.create_character(db, character_data, image_filename=image_filename, image_url=image_url)
    return RedirectResponse(url="/characters", status_code=303)

# Editar personaje (formulario)
@router.get("/characters/edit/{character_id}", response_class=HTMLResponse)
def edit_character_page(character_id: int, request: Request, db: Session = Depends(get_db)):
    character = crud.get_character(db, character_id)
    if not character:
        return RedirectResponse(url="/characters", status_code=303)
    return request.app.state.templates.TemplateResponse(
        "characters_edit.html",
        {"request": request, "character": character}
    )

# Actualizar personaje (POST)
@router.post("/characters/edit/{character_id}")
async def update_character_page(
    character_id: int,
    request: Request,
    name: str = Form(...),
    alias: str = Form(None),
    alignment: str = Form(...),
    description: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    image_filename = None
    image_url = None
    if image:
        content = await image.read()
        safe_name = f"characters/{name.replace(' ', '_')}_{image.filename}"
        image_url = upload_image_to_supabase(content, safe_name, content_type=image.content_type)
        image_filename = image.filename

    character_data = schemas.CharacterCreate(
        name=name,
        alias=alias,
        alignment=alignment,
        description=description,
        active=True
    )
    crud.update_character(db, character_id, character_data)

    # Actualizar imagen si se subió
    db_character = crud.get_character(db, character_id)
    if image_filename:
        db_character.image_filename = image_filename
    if image_url:
        db_character.image_url = image_url
    db.commit()
    db.refresh(db_character)

    return RedirectResponse(url="/characters", status_code=303)

# Eliminar personaje (soft delete)
@router.post("/characters/delete/{character_id}")
def delete_character_page(character_id: int, db: Session = Depends(get_db)):
    crud.soft_delete_character(db, character_id)
    return RedirectResponse(url="/characters", status_code=303)