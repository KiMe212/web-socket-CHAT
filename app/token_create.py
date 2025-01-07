import uuid

from datetime import datetime, timedelta
from jose import jwt

from fastapi import Depends, Header, HTTPException, status, Request, Response
from fastapi.responses import RedirectResponse

from sqlalchemy import select

from app.database import SessionLocal, get_session
from app.models.users import User

from jose import JWTError, jwt


from app.config import ACCESS_TOKEN_EXPIRE_TIME, SECRET_KEY, ALGORITHM,  REFRESH_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_SECRET_KEY


def create_access_token(data: dict, expiry_time: timedelta | None = None):
    to_encode = data.copy()
    if expiry_time:
        expire = datetime.utcnow() + expiry_time
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_TIME))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(REFRESH_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str, type: str = 'access') -> str | None:
    try:
        if type == 'refresh':
            payload = jwt.decode(token, REFRESH_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
        else:    
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  
        return payload
    except JWTError as EROOR:
        return None
    
    
def get_refersh_token(request: Request):
    cookie = request.cookies
    if not cookie:
        return None
    if cookie.get('refresh-Token'):
        return cookie.get('refresh-Token')
    

def update_access_token(request: Request, response: Response, session: SessionLocal = Depends(get_session)):
    refersh_token = get_refersh_token(request)
    payload_data = decode_token(token=refersh_token, type='refresh')
    print(f"{payload_data=}")
    if not payload_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Access and refraxh tokens is finishd")
        # return RedirectResponse("localhost:8000/login", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    name = payload_data.get("sub")
    if not name:
        return RedirectResponse("localhost:8000/login", status_code=status.HTTP_307_TEMPORARY_REDIRECT) 
    data_query = select(User.password, User.id).where(User.name == name)
    data_user = session.execute(data_query).mappings().first()
    if not data_user:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="User are not register"
    )
    token = create_access_token(data={"sub":name})
    response.headers["Authorization"] = token
    return data_user
    

def get_current_user(request: Request, response: Response, authorization: str = Header(None), session: SessionLocal = Depends(get_session)):
    token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"Jwt-Token": ""},)   
    if not authorization:
        raise token_exception
    payload_data: str = decode_token(authorization)

    if payload_data:
        name = payload_data.get("sub")
        if not name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Don't corкect token")
        data_query = select(User.password, User.id).where(User.name == name)
        data_user = session.execute(data_query).mappings().first()
        if not data_user:
            raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="User are not register"
    )
        return data_user
    else:
        return update_access_token(request, response, session)


def check_token():
    return "Hi"