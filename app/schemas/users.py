from pydantic import BaseModel, validator

from app.core.hasher import get_password_hash


class CreateUserSchema(BaseModel):
    name: str
    password: str

    @validator("password", pre=True)
    def hash_password(cls, password: str) -> str:
        return get_password_hash(password)


class LoginUserSchema(BaseModel):
    name: str
    password: str
