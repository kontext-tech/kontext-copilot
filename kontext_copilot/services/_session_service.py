from typing import Union

from fastapi import Depends
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker

from kontext_copilot.data.models import Session, SessionMessage
from kontext_copilot.data.schemas import (
    CreateSessionMessageModel,
    CreateSessionModel,
    SessionMessageModel,
    SessionModel,
    SessionUpdateModel,
    UpdateSessionMessageModel,
)
from kontext_copilot.services._utils import get_engine


class SessionService:

    def __init__(self, engine: Engine):
        """
        Initializes the SessionService with a given database engine.

        :param engine: The SQLAlchemy engine to be used for database operations.
        """
        self.engine = engine
        self.session_maker = sessionmaker(bind=self.engine)

    def create_session(self, session_create: CreateSessionModel) -> SessionModel:
        """
        Creates a new Session entity from a CreateSessionModel.

        :param session_create: The CreateSessionModel instance containing the data for the new Session.
        :return: The created SessionInitResponseModel instance.
        """
        with self.session_maker() as session:
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
        with self.session_maker() as session:
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
        with self.session_maker() as session:
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

    def add_session_message(
        self, session_id: int, message: CreateSessionMessageModel
    ) -> SessionMessageModel:
        """
        Adds a new message to a Session.

        :param session_id: The ID of the Session to add the message to.
        :param message: The CreateSessionMessageModel instance containing the data for the new message.
        :return: The created SessionMessageModel instance.
        """
        with self.session_maker() as session:
            # Retrieve the Session from the database
            session_db = (
                session.query(Session).filter(Session.id == session_id).one_or_none()
            )
            if session_db is None:
                raise ValueError(f"Session not found: {session_id}")
            # Convert CreateSessionMessageModel to SessionMessage, assuming model_dump() correctly prepares data for creation
            new_message_db = SessionMessage(**message.model_dump())
            # Add the new message to the session and commit changes
            session.add(new_message_db)
            session.commit()
            # Refresh the instance from the database to ensure it's up-to-date
            session.refresh(new_message_db)
            # Convert database model to Pydantic model
            return SessionMessageModel.from_db_model(new_message_db)

    def update_session_message(
        self,
        session_id: int,
        message_id: int,
        message_update: UpdateSessionMessageModel,
    ) -> SessionMessageModel:
        """
        Updates an existing message in a Session.

        :param session_id: The ID of the Session containing the message.
        :param message_id: The ID of the message to update.
        :param message_update: The UpdateSessionMessageModel instance containing the new data for the message.
        :return: The updated SessionMessageModel instance.
        """
        with self.session_maker() as session:
            # Retrieve the Session from the database
            session_db = (
                session.query(Session).filter(Session.id == session_id).one_or_none()
            )
            if session_db is None:
                raise ValueError(f"Session not found: {session_id}")
            # Retrieve the message from the database
            message_db = (
                session.query(SessionMessage)
                .filter(SessionMessage.id == message_id)
                .filter(SessionMessage.session_id == session_id)
                .one_or_none()
            )
            if message_db is None:
                raise ValueError(f"Message not found: {message_id}")
            # Update the message with the new data
            for field, value in message_update.model_dump(exclude_unset=True).items():
                setattr(message_db, field, value)
            # Commit changes
            session.commit()
            # Refresh the instance from the database to ensure it's up-to-date
            session.refresh(message_db)
            # Convert database model to Pydantic model
            return SessionMessageModel.from_db_model(message_db)

    def append_message_part(
        self,
        session_id: int,
        message_id: int,
        message_part: Union[str, bytes],
        done: bool = False,
    ) -> SessionMessageModel:
        """
        Appends a new part to an existing message in a Session.

        :param session_id: The ID of the Session containing the message.
        :param message_id: The ID of the message to update.
        :param message_part: The new part to append to the message.
        :return: The updated SessionMessageModel instance.
        """
        with self.session_maker() as session:
            # Retrieve the Session from the database
            session_db = (
                session.query(Session).filter(Session.id == session_id).one_or_none()
            )
            if session_db is None:
                raise ValueError(f"Session not found: {session_id}")
            # Retrieve the message from the database
            message_db = (
                session.query(SessionMessage)
                .filter(SessionMessage.id == message_id)
                .filter(SessionMessage.session_id == session_id)
                .one_or_none()
            )
            if message_db is None:
                raise ValueError(f"Message not found: {message_id}")
            # Append the new part to the message
            if message_db.content is None:
                message_db.content = message_part
            else:
                message_db.content += message_part
            message_db.done = done
            if done:
                message_db.generating = False
            # Commit changes
            session.commit()
            # Refresh the instance from the database to ensure it's up-to-date
            session.refresh(message_db)
            # Convert database model to Pydantic model
            return SessionMessageModel.from_db_model(message_db)


def get_session_service(
    engine: Engine = Depends(get_engine),
) -> SessionService:
    """
    Returns a SessionService instance with the provided engine.
    """
    return SessionService(engine)
