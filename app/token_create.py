import uuid

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy import select

from app.database import SessionLocal, get_session
from app.models.users import User


def create_token():
    print(uuid.uuid4())
    return str(uuid.uuid4())


def check_token(
    authorization: str = Header(None), session: SessionLocal = Depends(get_session)
):
    try:
        if authorization is not None:
            data_user = (
                session.execute(
                    select(User.name, User.id).where(
                        User.token == authorization.split()[1]
                    )
                )
                .mappings()
                .first()
            )
            if data_user:
                return data_user
            return False
        else:
            return False
    except IndexError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
