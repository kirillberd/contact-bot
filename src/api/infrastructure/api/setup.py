from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.container import Container
from infrastructure.api.controllers import main_controller

def load_continaer_config(container: Container):
    container.config.postgres_user.from_env("POSTGRES_USER")
    container.config.postgres_password.from_env("POSTGRES_PASSWORD")
    container.config.postgres_host.from_env("POSTGRES_HOST")
    container.config.postgres_port.from_env("POSTGRES_PORT", as_=str)
    container.config.postgres_dbname.from_env("POSTGRES_DBNAME")


def setup(app: FastAPI, container: Container):
    load_continaer_config(container=container)
    container.wire(modules=[main_controller])
    app.include_router(main_controller.router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )