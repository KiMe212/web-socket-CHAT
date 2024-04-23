from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import insert, select, update

from app.core.hasher import verify_password
from app.database import SessionLocal, get_session
from app.models.users import User
from app.schemas.users import CreateUserSchema, LoginUserSchema
from app.token_create import check_token, create_token

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

        return JSONResponse(content={"ID": user_id})
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="That name already exists"
    )


@auth_router.post("/login", status_code=status.HTTP_201_CREATED)
def login(data: LoginUserSchema, session: SessionLocal = Depends(get_session)):

    data_query = select(User.password, User.id).where(User.name == data.name)
    data_user = session.execute(data_query).mappings().first()

    if data_user is not None and verify_password(data.password, data_user["password"]):
        data_token = create_token()

        data_user = (
            update(User).where(User.id == data_user["id"]).values(token=data_token)
        )

        session.execute(data_user)
        session.commit()

        return JSONResponse(content={"Token": data_token})
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong password or name"
    )


@auth_router.delete("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    session: SessionLocal = Depends(get_session), user: dict = Depends(check_token)
):
    if user:
        data_user = (
            update(User)
            .where(User.id == user["id"])
            .values(token=None)
            .returning(User.id)
        )

        user_id = session.execute(data_user)
        session.commit()
        if user_id:
            return JSONResponse(content={"status": "Success"})
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="DB don't have your token",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="You are not auth"
        )
