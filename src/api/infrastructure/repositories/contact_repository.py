from abc import abstractmethod, ABC
from domain.contact import Contact
from typing import List, Optional
from dataclasses import dataclass
from sqlalchemy import Engine
from sqlmodel import select, delete, update, func
from ..providers.postgres_provider import PostgresContextProvider
from loguru import logger


class IContactRepository(ABC):

    @abstractmethod
    def add(self, contact: Contact) -> None: ...

    @abstractmethod
    def get(
        self, tags: Optional[List[str]] = None, region: Optional[str] = None
    ) -> List[Contact]: ...

    @abstractmethod
    def update(self, contact: Contact, id: int) -> None: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...


@dataclass
class ContactRepository(IContactRepository):

    engine: Engine

    def add(self, contact: Contact) -> None:
        with PostgresContextProvider(self.engine) as session:
            if session is None:
                logger.error("Error connecting to a database")
                raise Exception("Could not connect to a database")
            else:
                session.add(contact)
                logger.info(f"Contact with email {contact.email} added to a db.")

    def get(
        self, tags: Optional[List[str]] = None, region: Optional[str] = None
    ) -> List[Contact]:
        with PostgresContextProvider(self.engine) as session:
            if session is None:
                logger.error("Error connecting to a database")
                raise Exception("Could not connect to a database")
            else:
                statement = select(Contact)

                if tags:
                    statement = statement.where(func.arrayoverlap(Contact.tags, tags))

                if region:
                    statement = statement.where(Contact.region == region)

                result = [Contact.model_validate(contact) for contact in session.exec(statement).all()]
                logger.info(f"Fetched {len(result)} contacts.")
                return result

    def update(self, contact: Contact, id: int) -> None:
        with PostgresContextProvider(self.engine) as session:
            if session is None:
                logger.error("Error connecting to a database")
                raise Exception("Could not connect to a database")
            else:
                statement = (
                    update(Contact)
                    .where(Contact.id == id)
                    .values(**contact.model_dump())
                )

                session.exec(statement)
                logger.info(f"Updated task with id {id}")

    def delete(self, id: int) -> None:
        with PostgresContextProvider(self.engine) as session:
            if session is None:
                logger.error("Error connecting to a database")
                raise Exception("Could not connect to a database")
            else:
                statement = delete(Contact).where(Contact.id == id)
                session.exec(statement)
                logger.info(f"Deleted task with id {id}")
