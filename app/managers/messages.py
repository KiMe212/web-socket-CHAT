from app.managers.connection import connection_manager
from app.schemas.messages import ListMessages, Rooms


class OldMessagesManager:
    def __init__(self) -> None:
        self.messages_rooms: dict[Rooms, ListMessages] = {}

    def add_old_messages(self, room, name, message):
        self.messages_rooms[room] = self.messages_rooms.setdefault(room, []) + [
            (name, message)
        ]

    async def get_old_message(self, room):
        if self.messages_rooms:
            for i in self.messages_rooms[room]:
                msg = f"{i[0]}: {i[1]}"
                await connection_manager.user_rooms[room][-1].send_text(msg)


messages_manager = OldMessagesManager()
