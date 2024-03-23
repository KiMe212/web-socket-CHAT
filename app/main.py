from fastapi import FastAPI

from app.routers.web_socket import socket
from app.routers.auth import auth_router

app = FastAPI(title="CHAT", description="Web Socket", version="0.1")

app.include_router(socket)
app.include_router(auth_router)
