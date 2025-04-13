from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app import models, schemas
from app.core.security import get_password_hash, verify_password


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def count_users(db: Session) -> int:
    """Compte le nombre d'utilisateurs dans la base de données"""
    return db.query(models.User).count()


def delete_all_users(db: Session) -> None:
    """Supprime tous les utilisateurs de la base de données (pour les tests uniquement)"""
    db.query(models.User).delete()
    db.commit()


def create_user(db: Session, user_in: schemas.UserCreate) -> models.User:
    db_user = models.User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        is_active=user_in.is_active,
        is_admin=user_in.is_admin,
        created_at=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: models.User, user_in: schemas.UserUpdate) -> models.User:
    update_data = user_in.model_dump(exclude_unset=True)
    if "password" in update_data and update_data["password"]:
        update_data["hashed_password"] = get_password_hash(update_data["password"])
        del update_data["password"]
    for field, value in update_data.items():
        setattr(user, field, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, username: str, password: str) -> Optional[models.User]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def update_last_login(db: Session, user: models.User) -> models.User:
    user.last_login = datetime.utcnow()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def is_active(user: models.User) -> bool:
    return user.is_active


def is_admin(user: models.User) -> bool:
    return user.is_admin
