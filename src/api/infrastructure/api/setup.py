from fastapi import FastAPI
from .controllers import main_controller
from ..container import Contaner

def setup(app: FastAPI, container: Contaner):
    container.wire(modules=[main_controller])
    app.include_router(main_controller.router)