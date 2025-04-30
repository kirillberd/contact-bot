from sqlmodel import Session
from sqlalchemy import Engine
from loguru import logger


class PostgresContextProvider:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine
        self._session = None

    def __enter__(self):
        try:
            self._session = Session(self._engine)
            return self._session
        except Exception as e:
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            if exc_type:
                logger.error(f"Error making request to a db: {exc_type}, {exc_val}")
                self._session.rollback()
            else:
                self._session.commit()
            self._session.close()
            if exc_val:
                raise Exception(f"{exc_val}")
        return True
