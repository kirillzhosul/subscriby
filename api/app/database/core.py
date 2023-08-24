from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData

DB_URL = "sqlite:///./db.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
metadata = MetaData()
Base: type = declarative_base(metadata=metadata)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=True, bind=engine
)


def create_all() -> None:
    metadata.create_all(bind=engine)


def get_db() -> sessionmaker:  # type: ignore[misc]
    """
    Returns database session for making plain database requests.
    """
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
