"""
Endpoints spéciaux pour les tests uniquement
Ces routes ne doivent PAS être exposées en production
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import user as user_service
from app.schemas.user import UserCreate
from app.core.config import settings

# Créer un router avec un préfixe spécifique pour les tests
router = APIRouter(prefix="/test", tags=["tests"])

# Variable pour activer/désactiver les routes de test
TEST_ROUTES_ENABLED = settings.ENVIRONMENT.lower() != "production"


@router.post("/create-first-user", status_code=status.HTTP_201_CREATED)
async def create_first_admin_user(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint spécial pour créer le premier utilisateur admin
    Cet endpoint ne devrait être accessible qu'en environnement de test
    """
    # Vérifier si les routes de test sont activées
    if not TEST_ROUTES_ENABLED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Les routes de test ne sont pas accessibles en production"
        )
    
    # Vérifier si le premier utilisateur existe déjà
    existing_users = user_service.count_users(db)
    if existing_users > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Des utilisateurs existent déjà dans la base de données"
        )
    
    # Forcer l'utilisateur à être admin
    user_data = user_in.model_dump()
    user_data["is_admin"] = True
    
    # Créer l'utilisateur
    try:
        user = user_service.create_user(db, UserCreate(**user_data))
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création de l'utilisateur: {str(e)}"
        )


@router.post("/reset-database", status_code=status.HTTP_200_OK)
async def reset_database(db: Session = Depends(get_db)):
    """
    Endpoint pour réinitialiser la base de données pour les tests
    ATTENTION: Cela supprime toutes les données!
    """
    # Vérifier si les routes de test sont activées
    if not TEST_ROUTES_ENABLED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Les routes de test ne sont pas accessibles en production"
        )
    
    try:
        # Supprimer tous les utilisateurs (et leurs données liées via cascade)
        user_service.delete_all_users(db)
        return {"message": "Base de données réinitialisée avec succès"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la réinitialisation: {str(e)}"
        )
