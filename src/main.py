from typing import List, Optional
from fastapi import FastAPI, HTTPException
from schemas.models import Post

app = FastAPI()

my_posts = []

def find_post(id: int) -> Optional[dict]:
    """
    Function to find a post by id in the posts list.
    :param id: The id of the post to find.
    :return: The post with the given id if it exists; raises HTTPException if it does not exist.
    """
    post = next((post for post in my_posts if post["id"] == id), None)
    if post:
        return {"data": post}
    raise HTTPException(
        status_code=404, detail="Post not found - check if the id is correct"
    )


def get_max_id_from_posts() -> int:
    """
    Function to get the max id from the posts list.
    :return: The maximum id among the posts; 0 if there are no posts.
    """
    return max((post["id"] for post in my_posts), default=0)


@app.get("/status", status_code=200)
def root() -> dict:
    """Server status endpoint. Returns a status message."""
    return {"Message": "Server is running"}


@app.get("/posts")
def get_posts() -> dict:
    """
    Endpoint to get all the posts.
    :return: All posts in a dictionary under the 'data' key.
    """
    return {"data": my_posts}


@app.post("/posts")
async def create_post(post: Post) -> dict:
    """
    Endpoint to create a new post.
    :param post: Post input model.
    :return: The newly created post in a dictionary under the 'data' key.
    """
    post_dict = post.dict()
    max_id = get_max_id_from_posts()
    post_dict["id"] = max_id + 1
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/latest")
def get_latest_post() -> dict:
    """
    Endpoint to get the latest post.
    :return: The latest post in a dictionary under the 'data' key.
    """
    id = get_max_id_from_posts()
    data = find_post(int(id))
    return {"data": data}


@app.get("/posts/{id}")
def get_post_by_id(id: int) -> dict:
    """
    Endpoint to get a post by id.
    :param id: The id of the post to get.
    :return: The post with the given id in a dictionary under the 'data' key.
    """
    data = find_post(id)
    return {"data": data}
