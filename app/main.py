import uvicorn
from fastapi import FastAPI

from app.routers.auth import auth_router
from app.routers.web_socket import socket
from app.config import config

app = FastAPI(title="CHAT", description="Web Socket", version="0.1")

app.include_router(socket)
app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", **config.uvicorn.model_dump())
