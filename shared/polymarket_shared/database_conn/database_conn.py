from contextlib import contextmanager
import os
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_utils import database_exists, create_database

load_dotenv()

def get_database_url() -> str:
    """Construct database URL from environment variables."""
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    db = os.getenv("POSTGRES_DB")
    host = "timescaledb"  # Service name from docker-compose
    port = os.getenv("POSTGRES_PORT", "5432")
    
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"

def create_engine_with_retry(url: str, max_retries: int = 5) -> Engine:
    """Create SQLAlchemy engine with retry logic."""
    engine = create_engine(url)
    
    # Ensure database exists
    if not database_exists(engine.url):
        create_database(engine.url)
    
    return engine

class DatabaseManager:
    _engine: Engine | None = None
    _sessionmaker: sessionmaker | None = None

    @classmethod
    def initialize(cls, database_url: str | None = None) -> None:
        """Initialize database connection."""
        if database_url is None:
            database_url = get_database_url()
        
        if cls._engine is None:
            cls._engine = create_engine_with_retry(database_url)
            cls._sessionmaker = sessionmaker(bind=cls._engine)

    @classmethod
    def get_engine(cls) -> Engine:
        """Get SQLAlchemy engine instance."""
        if cls._engine is None:
            cls.initialize()
        return cls._engine

    @classmethod
    def get_session(cls) -> Session:
        """Get a new SQLAlchemy session."""
        if cls._sessionmaker is None:
            cls.initialize()
        return cls._sessionmaker()

    @classmethod
    @contextmanager
    def session_scope(cls) -> Generator[Session, None, None]:
        """Provide a transactional scope around a series of operations."""
        session = cls.get_session()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close() 