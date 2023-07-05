from typing import List, Optional
from fastapi import FastAPI, HTTPException, status, Response
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
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found"
    )


def get_max_id_from_posts() -> int:
    """
    Function to get the max id from the posts list.
    :return: The maximum id among the posts; 0 if there are no posts.
    """
    return max((post["id"] for post in my_posts), default=0)


@app.get("/status", status_code=status.HTTP_200_OK)
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


@app.post("/posts", status_code=status.HTTP_201_CREATED)
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


@app.get("/posts/{id}")
def get_post_by_id(id: int) -> dict:
    """
    Endpoint to get a post by id.
    :param id: The id of the post to get.
    :return: The post with the given id in a dictionary under the 'data' key.
    """
    data = find_post(id)
    return {"data": data}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    data = find_post(id)
    if data:
        global my_posts
        my_posts = [
            post for post in my_posts if post["id"] != id
        ]  # creates the array of data with everything but that id
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    existing_post = find_post(id)
    if existing_post:
        global my_posts
        my_posts = [post for post in my_posts if post["id"] != id]
        updated_post = existing_post["data"]
        update_data = post.dict(exclude_unset=True)
        updated_post.update(update_data)
        my_posts.append(updated_post)
        return {"response": "Post updated successfully", "data": updated_post}
