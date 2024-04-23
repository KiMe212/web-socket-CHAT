from fastapi import WebSocket

# from app.schemas.connection import Room, ListSocketUser


class ConnectionManager:
    def __init__(self):
        # self.user_rooms: dict[Room, ListSocketUser] = {}
        self.user_rooms: dict[str, list] = {}

    async def connect(self, websocket: WebSocket, room: str):
        await websocket.accept()
        self.user_rooms[room] = self.user_rooms.setdefault(room, []) + [websocket]

    async def broadcast_messages(self, room: str, messages: list):
        for msg in messages:
            await self.user_rooms[room][-1].send_text(msg)

    async def broadcast(self, room: str, message: str):
        for connection in self.user_rooms[room]:
            await connection.send_text(message)

    def disconnect(self, room: str, websocket: WebSocket):
        self.user_rooms[room].remove(websocket)


connection_manager = ConnectionManager()
