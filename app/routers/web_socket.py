from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, status, Header, Depends
from fastapi.responses import RedirectResponse 
from sqlalchemy import select
from app.models.users import User
from app.database import SessionLocal, get_session
from app.managers.connection import connection_manager
from app.managers.messages import messages_manager
from app.managers.rooms import room_manager

socket = APIRouter()


@socket.post("/room")
def create_room(
    name_room: str,
    authorization: str = Header(None),
    session: SessionLocal = Depends(get_session)
    ):
    if authorization is not None:
        data_user = session.execute(
            select(User.name).where(User.token == authorization[6:])
            ).mappings().first()
        session.commit()
        if data_user:
            try:
                room_manager.add_room(name_room, data_user["name"])
                return {"User-Agent":authorization}
            except:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="That room is exist"
                    )
        else:
            return RedirectResponse("localhost:8000/login")
    else:
        return RedirectResponse("localhost:8000/login")


@socket.delete("/room")
def delete_room(
    name_room:str,
    authorization: str = Header(None),
    session: SessionLocal = Depends(get_session)
    ):
    if authorization is not None:
        data_user = session.execute(
            select(User.name).where(User.token == authorization[6:])
            ).mappings().first()
        session.commit()

        if data_user:
            try:
                room_manager.remove_room(name_room, data_user["name"])
            except:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="That room is not exist"
                    )
        else:
            return RedirectResponse("localhost:8000/login")
    else:
        return RedirectResponse("localhost:8000/login")


@socket.websocket("/ws/{name_room}", )
async def websocket_endpoint(
    websocket: WebSocket,
    name_room: str,
    authorization: str = Header(None),
    session: SessionLocal = Depends(get_session)
    ):
    if authorization is not None:
        data_user = session.execute(
            select(User.name).where(User.token == authorization[6:])
            ).mappings().first()
        session.commit()
        if data_user:
            if name_room in connection_manager.user_rooms:
                await connection_manager.connect(websocket, name_room)
                await messages_manager.get_old_message(name_room)
                # await manager.crypt(name_room)
                try:
                    while True:
                        data = await websocket.receive_text()
                        user_name = data_user["name"]
                        await connection_manager.broadcast(name_room, f"{user_name}: {data}")
                        messages_manager.add_old_messages(name_room, user_name, data)
                except WebSocketDisconnect:
                    connection_manager.disconnect(name_room, websocket)
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="That room is not exist")
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You are not auth or don't have right"
                )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not auth"
            )

