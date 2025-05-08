from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from infrastructure.api.setup import setup
from infrastructure.container import Container
import os
from loguru import logger

API_KEY= os.environ.get("REACT_APP_AUTH_TOKEN")

def init():
    app = FastAPI()
    container = Container()
    app.extra = container
    setup(app, container)
    return app


app = init()

@app.middleware("http")
async def api_key_auth_middleware(request: Request, call_next):

    if request.method == "OPTIONS":
        return await call_next(request)
    api_key = request.headers.get("api-key")
    logger.debug(request.headers)

    if not api_key:
        return JSONResponse(
            status_code=401,
            content={"detail": "API key is missing. Use api-key header"},
        )


    if api_key != API_KEY:
        return JSONResponse(status_code=401, content={"detail": "Invalid API key"})

    return await call_next(request)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=4000, reload=False)
