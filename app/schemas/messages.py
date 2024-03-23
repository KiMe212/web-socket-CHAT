from pydantic import BaseModel


class Rooms(BaseModel):
    room: str


class Messages(BaseModel):
    name_and_message: tuple


class OldMessages(BaseModel):
    list_old_messages: list[Messages]
