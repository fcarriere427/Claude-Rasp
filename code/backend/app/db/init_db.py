import logging
from sqlalchemy.orm import Session

from app import schemas
from app.core.config import settings
from app.services import user as user_service


logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    """Initialize the database with first user"""
    # Check if we already have users
    users = user_service.get_users(db, limit=1)
    if users:
        logger.info("Database already initialized with users")
        return
    
    logger.info("Creating initial admin user")
    
    # Create admin user
    user_in = schemas.UserCreate(
        username="admin",
        email="admin@example.com",
        password="admin",  # This should be changed immediately
        is_active=True,
        is_admin=True,
    )
    
    user = user_service.create_user(db, user_in=user_in)
    logger.info(f"Admin user created with ID: {user.id}")

    logger.info("Initial database setup completed")
