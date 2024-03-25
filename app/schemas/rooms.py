from pydantic import BaseModel


class Creator(BaseModel):
    name: str


class Room(BaseModel):
    name: str


class ListRooms(BaseModel):
    list_rooms: list[Room]
