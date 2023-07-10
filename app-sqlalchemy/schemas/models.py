from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    """
    Pydantic model that defines the expected schema for a blog post.

    Attributes:
    title (str): Title of the blog post. This field is required.
    content (str): Content of the blog post. This field is required.
    published (bool): Indicates whether the post is published or not. This field is optional and defaults to True.
    """

    title: str
    content: str
    published: Optional[
        bool
    ] = True  # having the default value makes the field not necessary and defaults to true
