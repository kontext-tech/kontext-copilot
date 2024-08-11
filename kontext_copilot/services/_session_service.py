from typing import Union
from fastapi import Depends
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker

from kontext_copilot.data.models._db_models import Session
from kontext_copilot.data.schemas import (
    CreateSessionModel,
    SessionModel,
    SessionUpdateModel,
)
from kontext_copilot.services import get_db_engine


class SessionService:

    def __init__(self, engine: Engine):
        """
        Initializes the SessionService with a given database engine.

        :param engine: The SQLAlchemy engine to be used for database operations.
        """
        self.engine = engine
        self.sessionmaker = sessionmaker(bind=self.engine)

    def create_session(self, session_create: CreateSessionModel) -> SessionModel:
        """
        Creates a new Session entity from a CreateSessionModel.

        :param session_create: The CreateSessionModel instance containing the data for the new Session.
        :return: The created SessionInitResponseModel instance.
        """
        session = self.sessionmaker()
        # Convert CreateSessionModel to Session, assuming model_dump() correctly prepares data for creation
        new_session_db = Session(**session_create.model_dump())
        # Add the new Session to the session and commit changes
        session.add(new_session_db)
        session.commit()
        # Refresh the instance from the database to ensure it's up-to-date
        session.refresh(new_session_db)
        # Convert database model to Pydantic model
        return SessionModel.from_db_model(new_session_db)

    def get_session(self, session_id: int, raise_error: bool = True) -> SessionModel:
        """
        Retrieves a Session entity by its ID.

        :param session_id: The ID of the Session to retrieve.
        :return: The SessionModel instance representing the retrieved Session.
        """
        session = self.sessionmaker()
        # Retrieve the Session from the database
        session_db = (
            session.query(Session).filter(Session.id == session_id).one_or_none()
        )
        if session_db is None and raise_error:
            raise ValueError(f"Session not found: {session_id}")
        elif session_db is None:
            return None
        # Convert database model to Pydantic model
        return SessionModel.from_db_model(session_db)

    def update_session(
        self, session_id: int, session_update: SessionUpdateModel
    ) -> SessionModel:
        """
        Updates an existing Session entity with new data.

        :param session_id: The ID of the Session to update.
        :param session_update: The CreateSessionModel instance containing the new data for the Session.
        :return: The updated SessionModel instance.
        """
        session = self.sessionmaker()
        # Retrieve the Session from the database
        session_db = (
            session.query(Session).filter(Session.id == session_id).one_or_none()
        )
        if session_db is None:
            raise ValueError(f"Session not found: {session_id}")
        # Update the Session with the new data
        for field, value in session_update.model_dump(exclude_unset=True).items():
            setattr(session_db, field, value)
        # Commit changes
        session.commit()
        # Refresh the instance from the database to ensure it's up-to-date
        session.refresh(session_db)
        # Convert database model to Pydantic model
        return SessionModel.from_db_model(session_db)


def get_session_service(
    engine: Engine = Depends(get_db_engine),
) -> SessionService:
    """
    Returns a SessionService instance with the provided engine.
    """
    return SessionService(engine)
