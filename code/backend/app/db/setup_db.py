import logging

from app.db.base import Base
from app.db.init_db import init_db
from app.db.session import SessionLocal, engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    db = SessionLocal()
    try:
        # Create tables
        logger.info("Creating tables")
        Base.metadata.create_all(bind=engine)
        
        # Initialize data
        logger.info("Initializing data")
        init_db(db)
    finally:
        db.close()


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
