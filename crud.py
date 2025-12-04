from sqlalchemy.orm import Session, joinedload
import models, schemas
from typing import List, Optional
from datetime import date

def get_characters(db: Session, q: str = "", skip: int = 0, limit: int = 100) -> List[models.Character]:
    query = db.query(models.Character).filter(models.Character.active == True)
    if q:
        qlike = f"%{q.lower()}%"
        query = query.filter(models.Character.name.ilike(qlike) | models.Character.alias.ilike(qlike))
    return query.order_by(models.Character.id).offset(skip).limit(limit).all()

def get_character(db: Session, character_id: int) -> Optional[models.Character]:
    return db.query(models.Character).options(
        joinedload(models.Character.secret_identity),
        joinedload(models.Character.teams).joinedload(models.CharacterTeam.team)
    ).filter(models.Character.id == character_id).first()

def create_character(db: Session, character: schemas.CharacterCreate, image_filename: str = None, image_url: str = None) -> models.Character:
    db_character = models.Character(**character.dict())
    if image_filename:
        db_character.image_filename = image_filename
    if image_url:
        db_character.image_url = image_url
    db.add(db_character)
    db.commit()
    db.refresh(db_character)
    return db_character

def update_character(db: Session, character_id: int, character: schemas.CharacterCreate) -> Optional[models.Character]:
    db_character = get_character(db, character_id)
    if db_character:
        for key, value in character.dict().items():
            setattr(db_character, key, value)
        db.commit()
        db.refresh(db_character)
    return db_character

def soft_delete_character(db: Session, character_id: int) -> Optional[models.Character]:
    db_character = db.query(models.Character).filter(models.Character.id == character_id).first()
    if db_character:
        db_character.active = False
        db.commit()
        db.refresh(db_character)
    return db_character

def restore_character(db: Session, character_id: int) -> Optional[models.Character]:
    db_character = db.query(models.Character).filter(models.Character.id == character_id).first()
    if db_character:
        db_character.active = True
        db.commit()
        db.refresh(db_character)
    return db_character

def get_teams(db: Session, q: str = "", skip: int = 0, limit: int = 100) -> List[models.Team]:
    query = db.query(models.Team).filter(models.Team.active == True)
    if q:
        qlike = f"%{q.lower()}%"
        query = query.filter(models.Team.name.ilike(qlike))
    return query.order_by(models.Team.id).offset(skip).limit(limit).all()

def get_team(db: Session, team_id: int) -> Optional[models.Team]:
    return db.query(models.Team).options(joinedload(models.Team.members).joinedload(models.CharacterTeam.character)).filter(models.Team.id == team_id).first()

def create_team(db: Session, team: schemas.TeamCreate, image_filename: str = None, image_url: str = None) -> models.Team:
    db_team = models.Team(**team.dict())
    if image_filename:
        db_team.image_filename = image_filename
    if image_url:
        db_team.image_url = image_url
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def update_team(db: Session, team_id: int, team: schemas.TeamCreate) -> Optional[models.Team]:
    db_team = get_team(db, team_id)
    if db_team:
        for key, value in team.dict().items():
            setattr(db_team, key, value)
        db.commit()
        db.refresh(db_team)
    return db_team

def soft_delete_team(db: Session, team_id: int) -> Optional[models.Team]:
    db_team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if db_team:
        db_team.active = False
        db.commit()
        db.refresh(db_team)
    return db_team

def restore_team(db: Session, team_id: int) -> Optional[models.Team]:
    db_team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if db_team:
        db_team.active = True
        db.commit()
        db.refresh(db_team)
    return db_team

def get_identities(db: Session) -> List[models.SecretIdentity]:
    return db.query(models.SecretIdentity).all()

def get_identity(db: Session, identity_id: int) -> Optional[models.SecretIdentity]:
    return db.query(models.SecretIdentity).filter(models.SecretIdentity.id == identity_id).first()

def create_identity(db: Session, identity: schemas.SecretIdentityCreate) -> models.SecretIdentity:
    character = db.query(models.Character).filter(models.Character.id == identity.character_id).first()
    if not character:
        raise ValueError("Character not found")
    existing = db.query(models.SecretIdentity).filter(models.SecretIdentity.character_id == identity.character_id).first()
    if existing:
        raise ValueError("Character already has a SecretIdentity")
    db_identity = models.SecretIdentity(**identity.dict())
    db.add(db_identity)
    db.commit()
    db.refresh(db_identity)
    return db_identity

def update_identity(db: Session, identity_id: int, identity: schemas.SecretIdentityCreate) -> Optional[models.SecretIdentity]:
    db_identity = get_identity(db, identity_id)
    if db_identity:
        new_char_id = identity.character_id
        if new_char_id != db_identity.character_id:
            new_char = db.query(models.Character).filter(models.Character.id == new_char_id).first()
            if not new_char:
                raise ValueError("New Character id not found")
            other = db.query(models.SecretIdentity).filter(models.SecretIdentity.character_id == new_char_id).first()
            if other and other.id != identity_id:
                raise ValueError("New Character already has a SecretIdentity")
        for key, value in identity.dict().items():
            setattr(db_identity, key, value)
        db.commit()
        db.refresh(db_identity)
    return db_identity

def delete_identity(db: Session, identity_id: int):
    db_identity = get_identity(db, identity_id)
    if db_identity:
        db.delete(db_identity)
        db.commit()

def get_character_teams(db: Session) -> List[models.CharacterTeam]:
    return db.query(models.CharacterTeam).all()

def create_character_team(db: Session, ct: schemas.CharacterTeamCreate) -> models.CharacterTeam:
    character = db.query(models.Character).filter(models.Character.id == ct.character_id).first()
    team = db.query(models.Team).filter(models.Team.id == ct.team_id).first()
    if not character or not team:
        raise ValueError("Character or Team not found")
    exist = db.query(models.CharacterTeam).filter(models.CharacterTeam.character_id==ct.character_id, models.CharacterTeam.team_id==ct.team_id).first()
    if exist:
        raise ValueError("Relation already exists")
    db_ct = models.CharacterTeam(**ct.dict())
    db.add(db_ct)
    db.commit()
    db.refresh(db_ct)
    return db_ct

def delete_character_team(db: Session, ct_id: int):
    db_ct = db.query(models.CharacterTeam).filter(models.CharacterTeam.id == ct_id).first()
    if db_ct:
        db.delete(db_ct)
        db.commit()

def get_stats(db: Session):
    chars = db.query(models.Character).count()
    teams = db.query(models.Team).count()
    identities = db.query(models.SecretIdentity).count()
    return {"characters": chars, "teams": teams, "identities": identities}