from pydantic import BaseModel
from fastapi import Query
from enum import Enum

class Role(Enum):
    admin: str = "admin"
    personel: str = "personel"

class User(BaseModel):
    username: str
    password: str
    # email: str = Query(..., regex="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    # role: Role