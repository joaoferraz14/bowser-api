import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status, Response
from ..schemas.models import Post
from ..adapters.psql_database_manager import DatabaseManager
from dotenv import load_dotenv
from ..utils.utils import path_builder

load_dotenv()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_FOLDER = "../sql-statements"

app = FastAPI()

db_manager = DatabaseManager()
query_database = db_manager.connect_to_database()

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
    sql_file_path = path_builder(CURRENT_DIR, SQL_FOLDER, "get_all_posts.sql")
    with open(sql_file_path, "r") as query:
        query_database.execute_query(query.read())
        rows = query_database.fetch_all_rows()
    return {"data": rows}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post) -> dict:
    """
    Endpoint to create a new post.
    :param post: Post input model.
    :return: The newly created post in a dictionary under the 'data' key.
    """
    sql_file_path = path_builder(CURRENT_DIR, SQL_FOLDER, "create_new_post.sql")
    with open(sql_file_path, "r") as query:
        query = query.read()
        query_database.execute_query(query, (post.title, post.content, post.published))
    query_database.commit_changes_to_db()
    return {"data": post}


@app.get("/posts/{id}")
def get_post_by_id(id: int) -> dict:
    """
    Endpoint to get a post by id.
    :param id: The id of the post to get.
    :return: The post with the given id in a dictionary under the 'data' key.
    """
    data = find_post(id)
    return {"data": data}


from typing import Dict
from fastapi import Response


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int) -> Response:
    """
    Delete a post by its ID.

    Args:
        id (int): The ID of the post to delete.

    Returns:
        A 204 No Content HTTP status code if the post is found and deleted.
    """
    data = find_post(id)
    if data:
        global my_posts
        my_posts = [
            post for post in my_posts if post["id"] != id
        ]  # creates the array of data with everything but that id
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post) -> Dict[str, object]:
    """
    Update a post by its ID.

    Args:
        id (int): The ID of the post to update.
        post (Post): The new post data.

    Returns:
        A dictionary with a response message and the updated data if the post is found and updated.
    """
    existing_post = find_post(id)
    if existing_post:
        global my_posts
        my_posts = [post for post in my_posts if post["id"] != id]
        updated_post = existing_post["data"]
        update_data = post.dict(exclude_unset=True)
        updated_post.update(update_data)
        my_posts.append(updated_post)
        return {"response": "Post updated successfully", "data": updated_post}
