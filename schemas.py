from datetime import date
from pydantic import BaseModel, Field
from typing import List, Optional

class TeamBase(BaseModel):
    name: str = Field(..., min_length=2)
    founded_date: Optional[date] = None
    description: Optional[str] = None
    active: bool = True

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    id: int
    image_url: Optional[str] = None

    class Config:
        orm_mode = True

class SecretIdentityBase(BaseModel):
    real_name: str
    birth_date: Optional[date] = None
    place_of_birth: Optional[str] = None

class SecretIdentityCreate(SecretIdentityBase):
    character_id: int

class SecretIdentity(SecretIdentityBase):
    id: int
    character_id: int

    class Config:
        orm_mode = True

class CharacterTeamBase(BaseModel):
    character_id: int
    team_id: int

class CharacterTeamCreate(CharacterTeamBase):
    pass

class CharacterTeam(CharacterTeamBase):
    id: int
    character: Optional["Character"] = None
    team: Optional[Team] = None

    class Config:
        orm_mode = True

class CharacterBase(BaseModel):
    name: str = Field(..., min_length=2)
    alias: Optional[str] = None
    alignment: str = Field(..., min_length=3)
    first_appearance: Optional[date] = None
    description: Optional[str] = None
    active: bool = True

class CharacterCreate(CharacterBase):
    pass

class Character(CharacterBase):
    id: int
    secret_identity: Optional[SecretIdentity] = None
    teams: List[CharacterTeam] = []

    class Config:
        orm_mode = True