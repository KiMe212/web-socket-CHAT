from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.user_rooms: dict[str, list] = {}

    async def connect(self, websocket: WebSocket, room: str):
        await websocket.accept()
        if not self.user_rooms.get(room):
            self.user_rooms[room] = []
        self.user_rooms[room] = self.user_rooms.setdefault(room, []) + [websocket]

    async def broadcast_messages(self, room: str, message: list):
        for msg in message:
            await self.user_rooms[room][-1].send_text(msg)


    async def broadcast_new_user(self, room: str, message: list):
        for connection in self.user_rooms[room][:-1]:
            await connection.send_text(message)


    async def broadcast_delete_user(self, room: str, message: list):
        for connection in self.user_rooms[room]:
            await connection.send_text(message)


    async def broadcast_list_users(self, room: str, message: list):
        await self.user_rooms[room][-1].send_text(message)


    async def broadcast(self, room: str, message: str):
        for connection in self.user_rooms[room]:
            await connection.send_text(message)

    def disconnect(self, room: str, websocket: WebSocket):
        self.user_rooms[room].remove(websocket)


connection_manager = ConnectionManager()
