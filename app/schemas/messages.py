from pydantic import BaseModel


class Rooms(BaseModel):
    room: str


class Message(BaseModel):
    name_and_message: tuple


class ListMessages(BaseModel):
    list_messages: list[Message]
