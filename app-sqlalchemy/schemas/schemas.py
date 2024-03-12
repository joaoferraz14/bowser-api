from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class BasePost(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


class CreatePost(BasePost):
    pass


class UpdatePost(BasePost):
    pass


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostResponse(BasePost):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
