from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import ORJSONResponse
from sqlalchemy import insert, select, update

from app.core.hasher import verify_password
from app.database import SessionLocal, get_session
from app.models.users import User
from app.schemas.users import CreateUserSchema, LoginUserSchema
from app.token_create import create_access_token, create_refresh_token, get_current_user

auth_router = APIRouter(tags=["auth"])


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
def sign_up(data: CreateUserSchema, session: SessionLocal = Depends(get_session)):
    if (
        not session.execute(select(User.name).where(User.name == data.name))
        .mappings()
        .first()
    ):

        data_query = insert(User).values(**data.dict()).returning(User.id)
        user_id = session.scalars(data_query).first()
        session.commit()

        return ORJSONResponse(content={"ID": user_id})
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="That name already exists"
    )


@auth_router.post("/login", status_code=status.HTTP_201_CREATED)
def login(user: LoginUserSchema, session: SessionLocal = Depends(get_session)):

    data_query = select(User.password, User.id).where(User.name == user.name)
    data_user = session.execute(data_query).mappings().first()

    if data_user is not None and verify_password(user.password, data_user["password"]):

        token = create_access_token(user.name)
        refresh_token = create_refresh_token(user.name)
        
        response = ORJSONResponse({"token" : token}, status_code=200)
        response.set_cookie(key="refresh-Token", value=refresh_token)
        return response

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong password or name"
    )


@auth_router.delete("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    user: dict = Depends(get_current_user)
):
        if user:
            return ORJSONResponse(content={"status": "Success"})
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="DB don't have your token",
            )
