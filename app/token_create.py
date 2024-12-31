import uuid

from datetime import datetime, timedelta
from jose import jwt

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy import select

from app.database import SessionLocal, get_session
from app.models.users import User

from app.config import ACCESS_TOKEN_EXPIRE_TIME, SECRET_KEY, ALGORITHM,  REFRESH_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_SECRET_KEY


def create_access_token(data: dict, expiry_time: timedelta | None = None):
  to_encode = data.copy()
  if expiry_time:
    expire = datetime.utcnow() + expiry_time
  else:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def decode_token(token: str, key: str | None = None, type: str = 'access') -> str | None:
    try:
        if type == 'refresh':
            payload = jwt.decode(token, REFRESH_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
        else:    
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])     
        if key:
            return payload.get(key)
        return payload.get('sub')
    except JWTError as e:
        print(e)
        return None

# def create_token():
#     print(uuid.uuid4())
#     return str(uuid.uuid4())


# def check_token(
#     authorization: str = Header(None), session: SessionLocal = Depends(get_session)
# ):
#     try:
#         if authorization is not None:
#             data_user = (
#                 session.execute(
#                     select(User.name, User.id).where(
#                         User.token == authorization.split()[1]
#                     )
#                 )
#                 .mappings()
#                 .first()
#             )
#             if data_user:
#                 return data_user
#             return False
#         else:
#             return False
#     except IndexError:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
