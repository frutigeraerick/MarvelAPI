from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    founded_date = Column(Date, nullable=True)
    description = Column(String, nullable=True)
    image_filename = Column(String, nullable=True)  
    image_url = Column(String, nullable=True)      
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    members = relationship("CharacterTeam", back_populates="team", cascade="all, delete-orphan")

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    alias = Column(String(100), nullable=True)
    alignment = Column(String(50), nullable=False)
    first_appearance = Column(Date, nullable=True)
    description = Column(String, nullable=True)
    image_filename = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    teams = relationship("CharacterTeam", back_populates="character", cascade="all, delete-orphan")
    secret_identity = relationship("SecretIdentity", back_populates="character", uselist=False, cascade="all, delete-orphan")

class SecretIdentity(Base):
    __tablename__ = "secret_identities"

    id = Column(Integer, primary_key=True, index=True)
    real_name = Column(String(100), nullable=False)
    birth_date = Column(Date, nullable=True)
    place_of_birth = Column(String(100), nullable=True)
    character_id = Column(Integer, ForeignKey("characters.id"), unique=True)

    character = relationship("Character", back_populates="secret_identity")

class CharacterTeam(Base):
    __tablename__ = "character_team"

    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"))
    team_id = Column(Integer, ForeignKey("teams.id"))

    character = relationship("Character", back_populates="teams")
    team = relationship("Team", back_populates="members")