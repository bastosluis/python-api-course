from passlib.context import CryptContext
from datetime import datetime, timedelta, UTC
from ..models.jwt_user import JWTUser
import jwt
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from bookstoreAPI.utils.const import *
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

pwd_context = CryptContext(schemes=["bcrypt"])
oauth_schema = OAuth2PasswordBearer(tokenUrl="/token")

jwt_user1 = {"username": "user1",
             "password": "$2b$12$sW6w1cD3NCgBk6k035Bdu.ARkTWWB0/.aOMfuaLrV/li7Tf0IfoQm",
             "disabled":False,
            #  "email": "email@email.com",
             "role": "admin"
             }
mock_jwt_user1 = JWTUser(**jwt_user1)

def get_hashed_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        return False

# Authenticate username and password to give JWT token
def authenticate_user(user:JWTUser):
    if mock_jwt_user1.username == user.username and verify_password(user.password, mock_jwt_user1.password):
        # user.role = "admin"
        return user
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

# Create access JWT token
def create_jwt_token(user:JWTUser):
    expiration = datetime.now(UTC) + timedelta()
    jwt_payload={"sub": user.username,
                 "exp": expiration}
    jwt_token = jwt.encode(jwt_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return {"token": jwt_token}
# Check whether JWT token is correct
def check_jwt_token(token: str = Depends(oauth_schema)):
    try: 
        jwt_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms= JWT_ALGORITHM)
        username = jwt_payload.get("sub")
        role = jwt_payload.get("role")
        expiration = jwt_payload.get("exp")
        if datetime.now(UTC) < expiration and mock_jwt_user1.username == username:
            return final_checks(username, role)
    except Exception as e:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

# Last check and final result
def final_checks(username:str, role:str):
    if role =="admin":
        return True
    return False