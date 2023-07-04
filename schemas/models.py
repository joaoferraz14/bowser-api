from pydantic import BaseModel
from typing import Optional

# define expected schema for the post
class Post(BaseModel):
    title: str
    content: str
    published: bool = True # having the default value makes the field not necessary and defaults to true
    rating: Optional[int] = None