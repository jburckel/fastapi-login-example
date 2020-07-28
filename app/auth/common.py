from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import TypeVar

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app import database, exception, crud, model
from app.setting import settings

UserModelType = TypeVar("UserModelType", bound=model.User)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token/")


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        str(settings.JWT_SECRET_KEY),
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token, str(settings.JWT_SECRET_KEY),
            algorithms=[settings.JWT_ALGORITHM]
        )
    except JWTError:
        raise exception.jwt_validation_fail
    return payload.get("sub")


def get_access_token(user_id: int) -> dict:
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRATION)
    access_token = create_access_token(
        data={"sub": str(user_id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(database.get_db)
) -> UserModelType:

    id = decode_access_token(token)
    if id is None:
        raise exception.jwt_validation_fail
    user = crud.user.get(db, id=id)
    if user is None:
        raise exception.jwt_validation_fail
    if getattr(user, 'is_active', False) is False:
        raise exception.deactivated_user
    return user
