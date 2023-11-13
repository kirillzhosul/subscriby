"""
    Core service for database, dependencies, engine and etc
"""
from typing import Callable, TypeVar

from fastapi import Depends
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import QueuePool

from app.settings import get_settings

T = TypeVar("T")

engine = create_engine(
    url=get_settings().database.postgres_dsn,
    max_overflow=0,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_timeout=10,
    pool_size=20,
    poolclass=QueuePool,
)

metadata = MetaData()
Base: type = declarative_base(metadata=metadata)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=True, bind=engine
)


def create_all() -> None:
    """
    Current alternative to migration, will create all required database tables
    """
    metadata.create_all(bind=engine)


def get_db() -> sessionmaker:  # type: ignore[misc]
    """
    Returns database session for making plain database requests
    """
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


def get_repository(repo_type: type[T]) -> Callable[[Session], T]:
    """
    Instantiates repository dependency (wrapped) based on type
    (Returns function that instantiates repository with given type)
    """

    def wrapper(db: Session = Depends(get_db)) -> T:
        return repo_type(db)  # type: ignore[call-arg]

    return wrapper
