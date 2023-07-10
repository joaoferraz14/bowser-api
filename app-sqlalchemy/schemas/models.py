from pydantic import BaseModel
from typing import Optional



class BasePost(BaseModel):
    title: str
    content: str
    published: Optional[
        bool
    ] = True 


class CreatePost(BasePost):
    pass


class UpdatePost(BasePost):
    pass


class PostResponse(BaseModel):
    title: str
    content: str
    published: bool
    class Config:
        orm_mode=True