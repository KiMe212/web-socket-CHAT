from pydantic import BaseModel


class RoomSchema(BaseModel):
    name: str
