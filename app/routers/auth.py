from fastapi import APIRouter, Depends, status, HTTPException, Response, Header
from fastapi.security import OAuth2PasswordBearer
from app.schemas.users import CreateUser, LoginUser
from app.models.users import User
from app.database import get_session, SessionLocal
from sqlalchemy import insert, select, update
from app.core.hasher import verify_password
from app.token_create import create_token
from app.database import Base, engine


auth_router = APIRouter(tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@auth_router.post('/signup', status_code=status.HTTP_200_OK)
def sing_up(data: CreateUser, session: SessionLocal = Depends(get_session)): # not use Depends
    if not session.execute(select(User.name).where(User.name == data.name)).mappings().first():
        
        data_query = insert(User).values(**data.dict()).returning(User.id)
        user_id = session.scalars(data_query).first()
        session.commit()

        return{"ID": user_id}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="That name already exists")


@auth_router.post('/login', status_code=status.HTTP_200_OK)
def login(data:LoginUser, session: SessionLocal = Depends(get_session)):

    data_query = select(User.password, User.id).where(User.name == data.name)
    data_user = session.execute(data_query).mappings().first()
    
    if data_user is not None and verify_password(data.password, data_user["password"]):
        data_token = create_token()

        data_user = update(User).where(User.id == data_user["id"]).values(token=data_token)

        session.execute(data_user)
        session.commit()

        return Response(status_code=status.HTTP_200_OK, headers={"Authorization":f"Token {data_token}"},content="You are in")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong password or name")


@auth_router.delete("/logout")
def logout(authorization: str = Header(None),session: SessionLocal = Depends(get_session)):
    if authorization is not None:
        data_user = session.execute(
            select(User.id).where(User.token == authorization[6:])
            ).mappings().first()
        session.commit()
        if data_user:
            try:
                data_user = update(User).where(User.id == data_user["id"]).values(token=None)

                session.execute(data_user)
                session.commit()
            except:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="don't have in DB")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are not auth")