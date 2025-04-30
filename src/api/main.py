from fastapi import FastAPI
import uvicorn
from infrastructure.api.setup import setup
from infrastructure.container import Container


def init():
    app = FastAPI()
    container = Container()
    app.extra = container
    setup(app, container)
    return app


app = init()
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=4000, reload=False)
