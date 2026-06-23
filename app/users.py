from sqlalchemy.orm import Session
from app import models
from app.auth import hash_password

def create_user(db: Session, name: str, email: str, password: str, role: str = "employee"):
    hashed = hash_password(password)
    db_user = models.User(
        name=name,
        email=email,
        password=hashed,
        role=role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(
        models.User.email == email
    ).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(
        models.User.id == user_id
    ).first()