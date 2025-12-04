from fastapi import APIRouter, Request, Depends, UploadFile, File, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import os
import crud, schemas
from database import get_db
from supabase_client import upload_image_to_supabase

router = APIRouter(tags=["Web Pages"])

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return request.app.state.templates.TemplateResponse("index.html", {"request": request})

@router.get("/characters", response_class=HTMLResponse)
def characters_page(request: Request, db: Session = Depends(get_db), q: str = ""):
    characters = crud.get_characters(db, q=q)
    return request.app.state.templates.TemplateResponse("characters_list.html", {
        "request": request,
        "characters": characters,
        "q": q
    })

@router.get("/characters/new", response_class=HTMLResponse)
def new_character_page(request: Request):
    return request.app.state.templates.TemplateResponse("characters_new.html", {"request": request})

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
    new_char = crud.create_character(db, character_data, image_filename=image_filename, image_url=image_url)
    return RedirectResponse(url="/characters", status_code=303)

@router.get("/teams", response_class=HTMLResponse)
def teams_page(request: Request, db: Session = Depends(get_db), q: str = ""):
    teams = crud.get_teams(db, q=q)
    return request.app.state.templates.TemplateResponse("teams_list.html", {
        "request": request,
        "teams": teams,
        "q": q
    })

@router.get("/teams/new", response_class=HTMLResponse)
def new_team_page(request: Request):
    return request.app.state.templates.TemplateResponse("teams_new.html", {"request": request})

@router.post("/teams/new")
async def create_team_page(
    request: Request,
    name: str = Form(...),
    founded_date: str = Form(None),
    description: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    image_filename = None
    image_url = None

    if image:
        content = await image.read()
        safe_name = f"teams/{name.replace(' ', '_')}_{image.filename}"
        image_url = upload_image_to_supabase(content, safe_name, content_type=image.content_type)
        image_filename = image.filename

    team_schema = schemas.TeamCreate(
        name=name,
        founded_date=founded_date,
        description=description,
        active=True
    )

    crud.create_team(db, team_schema, image_filename=image_filename, image_url=image_url)

    return RedirectResponse(url="/teams", status_code=303)

@router.get("/character_team/list", response_class=HTMLResponse)
def character_team_list_page(request: Request, db: Session = Depends(get_db)):
    relations = crud.get_character_teams(db)
    return request.app.state.templates.TemplateResponse(
        "character_team_list.html",
        {"request": request, "relations": relations}
    )

@router.get("/character_team/new", response_class=HTMLResponse)
def character_team_new_page(request: Request, db: Session = Depends(get_db)):
    characters = crud.get_characters(db)
    teams = crud.get_teams(db)
    return request.app.state.templates.TemplateResponse(
        "character_team_new.html",
        {"request": request, "characters": characters, "teams": teams}
    )

@router.post("/character_team/new")
def create_character_team_page(
    request: Request,
    character_id: int = Form(...),
    team_id: int = Form(...),
    db: Session = Depends(get_db)
):
    ct = schemas.CharacterTeamCreate(character_id=character_id, team_id=team_id)
    crud.create_character_team(db, ct)
    return RedirectResponse(url="/character_team/list", status_code=303)

@router.get("/identities", response_class=HTMLResponse)
def identities_page(request: Request, db: Session = Depends(get_db)):
    identities = crud.get_identities(db)
    return request.app.state.templates.TemplateResponse("identities_list.html", {
        "request": request,
        "identities": identities
    })

@router.get("/identities/new", response_class=HTMLResponse)
def identity_new_page(request: Request, db: Session = Depends(get_db)):
    characters = crud.get_characters(db)
    return request.app.state.templates.TemplateResponse(
        "identities_new.html",
        {"request": request, "characters": characters}
    )

@router.post("/identities/new")
def create_identity_page(
    request: Request,
    character_id: int = Form(...),
    real_name: str = Form(...),
    birth_date: str = Form(None),
    place_of_birth: str = Form(None),
    db: Session = Depends(get_db)
):
    identity = schemas.SecretIdentityCreate(
        character_id=character_id,
        real_name=real_name,
        birth_date=birth_date,
        place_of_birth=place_of_birth
    )

    crud.create_identity(db, identity)

    return RedirectResponse(url="/identities", status_code=303)



@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    stats = crud.get_stats(db)
    return request.app.state.templates.TemplateResponse("dashboard.html", {
        "request": request,
        "stats": stats
    })
