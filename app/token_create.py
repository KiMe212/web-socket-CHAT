import uuid

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy import select

from app.database import SessionLocal, get_session
from app.models.users import User

from datetime import datetime, timedelta
from jose import jwt
from app.config import ACCESS_TOKEN_EXPIRE_TIME, SECRET_KEY, ALGORITHM
# for refresh tokens
from app.config import REFRESH_TOKEN_EXPIRE_TIME, REFRESH_TOKEN_SECRET_KEY
def create_access_token(data: dict, expiry_time: timedelta | None = None):
  to_encode = data.copy()
  if expiry_time:
    expire = datetime.utcnow() + expiry_time
  else:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

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
