from fastapi import Depends
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker

from kontext_copilot.data.models._db_models import Session
from kontext_copilot.data.schemas import CreateSessionModel, SessionModel
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
        new_session = Session(**session_create.model_dump())
        # Add the new Session to the session and commit changes
        session.add(new_session)
        session.commit()
        # Refresh the instance from the database to ensure it's up-to-date
        session.refresh(new_session)
        # Convert database model to Pydantic model
        return SessionModel.from_db_model(new_session)


def get_session_service(
    engine: Engine = Depends(get_db_engine),
) -> SessionService:
    """
    Returns a SessionService instance with the provided engine.
    """
    return SessionService(engine)
