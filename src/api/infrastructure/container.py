from dependency_injector.containers import DeclarativeContainer
from dependency_injector import providers
from sqlalchemy import Engine
from sqlmodel import create_engine
from infrastructure.repositories.contact_repository import ContactRepository

class Container(DeclarativeContainer):

    config = providers.Configuration()


    sql_engine: Engine = providers.Singleton(
        create_engine,
        url=providers.Callable(
                       lambda user, password, host, port, dbname: f"postgresql://{user}:{password}@{host}:{port}/{dbname}",
            config.postgres_user,
            config.postgres_password,
            config.postgres_host,
            config.postgres_port,
            config.postgres_dbname,
        )
    )

    contact_repository: ContactRepository = providers.Singleton(
        ContactRepository, engine=sql_engine
    )

