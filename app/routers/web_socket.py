from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy import delete, insert, select

from app.database import SessionLocal, get_session
from app.managers.connection import connection_manager
from app.models.messages import Message
from app.models.rooms import Room
from app.models.users import User
from app.models.users_room import UsersRoom
from app.schemas.rooms import RoomSchema
from app.token_create import check_token

socket = APIRouter()


@socket.post("/room", status_code=status.HTTP_201_CREATED)
def create_room(
    new_room: RoomSchema,
    user: dict = Depends(check_token),
    session: SessionLocal = Depends(get_session),
):
    if user:
        # check that room isn't exist
        if not (
            session.execute(select(Room.id).where(Room.name == new_room.name))
            .mappings()
            .first()
        ):
            try:
                # create room
                data_query = (
                    insert(Room)
                    .values(name=new_room.name, user_id=user["id"])
                    .returning(Room.id)
                )
                room_id = session.scalars(data_query).first()
                session.commit()
                return JSONResponse(content={"room_id": room_id})
            except RuntimeError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Something went bad"
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="That room is exist"
            )
    else:
        return RedirectResponse("localhost:8000/login")


@socket.delete("/room", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(
    room: RoomSchema,
    user: dict = Depends(check_token),
    session: SessionLocal = Depends(get_session),
):
    if user:
        # check that room is exist
        room_data = (
            session.execute(select(Room.user_id).where(Room.name == room.name))
            .mappings()
            .first()
        )
        if room_data:
            # check what that user can delete the room
            if room_data["user_id"] == user["id"]:
                try:
                    # delete room
                    data_query = (
                        delete(Room).where(Room.name == room.name).returning(Room.id)
                    )
                    room_id = session.scalars(data_query).first()
                    session.commit()
                    # delete room from user_room that have websocket
                    if connection_manager.user_rooms.get(room.name):
                        del connection_manager.user_rooms[room.name]
                    return JSONResponse(content={"room_id": room_id})
                except RuntimeError:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Something went bad",
                    )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You don't have right",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="That room is exist"
            )
    else:
        return RedirectResponse("localhost:8000/login")


@socket.get("/room", status_code=status.HTTP_200_OK)
def get_all_rooms(session: SessionLocal = Depends(get_session)):
    data_query = select(Room.name)
    rooms = session.execute(data_query).fetchall()
    all_rooms = [i[0] for i in rooms]
    return JSONResponse(content=all_rooms)


@socket.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    room: str,
    user: dict = Depends(check_token),
    session: SessionLocal = Depends(get_session),
):
    if user:
        # check the room
        data_query = select(Room.name, Room.id).where(Room.name == room)
        data_room = session.execute(data_query).mappings().first()
        if room == data_room["name"]:

            # connect
            await connection_manager.connect(websocket, room)

            # add new user in room
            data_query = (
                insert(UsersRoom)
                .values(room_id=data_room["id"], user_id=user["id"])
                .returning(UsersRoom.id)
            )
            session.scalars(data_query).first()
            session.commit()

            # get all users from room
            data_query = (
                select(UsersRoom.id, User.name)
                .join(User, UsersRoom.user_id == User.id)
                .where(UsersRoom.room_id == data_room["id"])
            )
            all_users = session.execute(data_query).mappings().all()
            users_room = "\n".join([i["name"] for i in all_users])
            await connection_manager.broadcast_list_users(
                room, (f"Users is online:\n {users_room}")
            )

            # get old messages
            data_query = select(Message.user_name, Message.message).where(
                Message.room_id == data_room["id"]
            )
            old_message = session.execute(data_query).mappings().all()
            all_message = [(f"{i['user_name']}: {i['message']}") for i in old_message]
            await connection_manager.broadcast_messages(room, all_message)

            # show new user
            user_name = user["name"]
            await connection_manager.broadcast_new_user(
                room, (f"User {user_name} entered the room")
            )

            try:
                while True:

                    # send message
                    data = await websocket.receive_text()
                    await connection_manager.broadcast(room, f"{user_name}: {data}")
                    if data:

                        # add message in room
                        data_query = (
                            insert(Message)
                            .values(
                                user_name=user["name"],
                                message=data,
                                status="ONLINE",
                                room_id=data_room["id"],
                            )
                            .returning(Message.id)
                        )
                        data = session.execute(data_query)
                        session.commit()
            except WebSocketDisconnect:
                connection_manager.disconnect(room, websocket)
                session.execute(
                    delete(UsersRoom)
                    .where(UsersRoom.user_id == user["id"])
                    .where(UsersRoom.room_id == data_room["id"])
                )
                session.commit()
                await connection_manager.broadcast_delete_user(
                    room, (f"User {user_name} exited the room")
                )

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="That room is not exist",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not auth or don't have right",
        )
