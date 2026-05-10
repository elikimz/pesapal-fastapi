"""Database configuration and session management."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import get_settings

settings = get_settings()

# Create engine with SQLite fallback for development
db_url = settings.database_url
if not db_url.startswith('postgresql'):
    db_url = 'sqlite:///./test.db'

engine = create_engine(
    db_url,
    echo=settings.debug,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False} if 'sqlite' in db_url else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    """Get database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
