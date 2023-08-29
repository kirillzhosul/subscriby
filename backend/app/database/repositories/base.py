from abc import ABC

from sqlalchemy.orm import Session
from app.database.core import Base


class BaseRepository(ABC):
    """
    Base repository without any implementation.
    Pretty weird.
    """

    pass


class SQLRepository(BaseRepository):
    """
    Base SQL repository that uses SQLAlchemy under the hood
    """

    # Database session and model to work with.
    db: Session
    model: Base

    def __init__(self, db: Session, model: Base) -> None:
        """
        Construct SQLRepository with given context (SQLAlchemy session and model).
        """
        self.db = db
        self.model = model
        if not isinstance(db, Session):
            raise TypeError(
                "SQL Repository expected database to be SQLAlchemy session!"
            )
        super().__init__()
