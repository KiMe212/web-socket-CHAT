from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.user_rooms: dict[str, list] = {}

    async def connect(self, websocket: WebSocket, room: str):
        await websocket.accept()
        self.user_rooms[room] = self.user_rooms.setdefault(room, []) + [websocket]

    async def broadcast(self, room, message: str):
        for connection in self.user_rooms[room]:
            await connection.send_text(message)

    def disconnect(self, room, websocket: WebSocket):
        self.user_rooms[room].remove(websocket)


connection_manager = ConnectionManager()
