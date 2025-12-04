import os
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

load_dotenv()

import models
from database import engine
from routers import characters, teams, identities, character_team, report
from web_routes import pages

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Marvel API + Frontend HTML")


templates = Jinja2Templates(directory="templates")

app.state.templates = templates

app.include_router(characters.router, prefix="/api")
app.include_router(teams.router, prefix="/api")
app.include_router(identities.router, prefix="/api")
app.include_router(character_team.router, prefix="/api")
app.include_router(report.router, prefix="/api")

app.include_router(pages.router)

@app.get("/health")
def health():
    return {"status": "ok"}