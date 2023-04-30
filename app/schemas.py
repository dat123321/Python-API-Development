from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id: Optional[int]
    user: str
    password: str


class User_out(BaseModel):
    id: int
    user: str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    user: str
    password: str


class Produce(BaseModel):
    name_produce: str
    quantity_produce: int


class Produce_out(Produce):
    id: int
    created_at: datetime
    owner: User_out

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    type: str


class TokenData(BaseModel):
    id: Optional[str] = None
