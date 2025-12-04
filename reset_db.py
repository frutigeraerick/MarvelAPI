from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
import models

def reset_db(db: Session):
    print("Borrando Character-Team...")
    db.query(models.CharacterTeam).delete()
    
    print("Borrando Secret Identities...")
    db.query(models.SecretIdentity).delete()
    
    print("Borrando Characters...")
    db.query(models.Character).delete()
    
    print("Borrando Teams...")
    db.query(models.Team).delete()
    
    print("Reiniciando IDs...")
    db.execute(text("ALTER SEQUENCE character_team_id_seq RESTART WITH 1;"))
    db.execute(text("ALTER SEQUENCE secret_identities_id_seq RESTART WITH 1;"))
    db.execute(text("ALTER SEQUENCE characters_id_seq RESTART WITH 1;"))
    db.execute(text("ALTER SEQUENCE teams_id_seq RESTART WITH 1;"))
    
    db.commit()
    print("Base de datos reseteada con exito.")

if __name__ == "__main__":
    db = next(get_db())
    reset_db(db)
