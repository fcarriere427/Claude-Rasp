from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

from app.core.config import settings

# Déterminer le chemin racine du projet
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '..'))

# Construire le chemin de la base de données
if settings.DATABASE_URL.startswith('sqlite:///./storage/'):
    # Chemin relatif à la racine du projet
    db_url = f"sqlite:///{os.path.join(PROJECT_ROOT, settings.DATABASE_URL[12:])}"
    print(f"Using database at: {db_url}")
    
    # Assurer que le répertoire existe
    db_path = db_url.replace('sqlite:///', '')
    db_dir = os.path.dirname(db_path)
    os.makedirs(db_dir, exist_ok=True)
else:
    # Utiliser l'URL telle quelle
    db_url = settings.DATABASE_URL
    print(f"Using database URL: {db_url}")

engine = create_engine(
    db_url, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
