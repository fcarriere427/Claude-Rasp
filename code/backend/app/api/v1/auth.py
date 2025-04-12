from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models, schemas
from app.api.deps.auth import get_current_active_admin, get_current_active_user
from app.core import security
from app.core.config import settings
from app.db.session import get_db
from app.services import user as user_service

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login", response_model=schemas.TokenResponse)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = user_service.authenticate_user(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user_service.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    
    # Update last login
    user = user_service.update_last_login(db, user)
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
        "user": user
    }


@router.post("/logout")
def logout(current_user: models.User = Depends(get_current_active_user)) -> Any:
    """
    Logout current user
    """
    # In the V1, logout is handled client-side
    # In the V2, we could add the token to a blacklist
    return {"message": "Déconnexion réussie"}


@router.post("/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def register(
    *,
    db: Session = Depends(get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(get_current_active_admin),
) -> Any:
    """
    Create new user (admin only in V1)
    """
    # Check if admin
    if not user_service.is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )
    
    # Check if the username exists
    user = user_service.get_user_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered",
        )
    
    # Check if the email exists
    user = user_service.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )
    
    # Create the user
    user = user_service.create_user(db, user_in=user_in)
    
    return user


@router.get("/me", response_model=schemas.User)
def read_users_me(
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user
    """
    return current_user


@router.put("/password")
def change_password(
    *,
    db: Session = Depends(get_db),
    current_password: str = Body(...),
    new_password: str = Body(...),
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    """
    Change current user password
    """
    # Verify current password
    if not security.verify_password(current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )
    
    # Update password
    user_in = schemas.UserUpdate(password=new_password)
    user = user_service.update_user(db, user=current_user, user_in=user_in)
    
    return {"message": "Mot de passe modifié avec succès"}
