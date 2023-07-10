import os
import json
from typing import Optional, Dict
from fastapi import FastAPI, HTTPException, status, Response, Depends
from ..schemas.models import Post
from ..handlers.psql_database_manager import DatabaseManager
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from ..utils.utils import path_builder


load_dotenv()



CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_FOLDER = "../sql-statements"

app = FastAPI()

db_manager = DatabaseManager()
query_database = db_manager.connect_to_database()


def find_post(id: int) -> Optional[dict]:
    """
    Function to find a post by id in the posts list.
    :param id: The id of the post to find.
    :return: The post with the given id if it exists; raises HTTPException if it does not exist.
    """
    with open(
        path_builder(CURRENT_DIR, SQL_FOLDER, "get_post_by_id.sql"), "r"
    ) as query:
        query_database.execute_query(query.read(), (id,))
        post = query_database.fetch_all_rows()
    if post:
        return {"data": post}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found"
    )


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
    with open(path_builder(CURRENT_DIR, SQL_FOLDER, "get_all_posts.sql"), "r") as query:
        query_database.execute_query(query.read())
    return {"data": query_database.fetch_all_rows()}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post) -> dict:
    """
    Endpoint to create a new post.
    :param post: Post input model.
    :return: The newly created post in a dictionary under the 'data' key.
    """
    with open(
        path_builder(CURRENT_DIR, SQL_FOLDER, "create_new_post.sql"), "r"
    ) as query:
        query_database.execute_query(
            query.read(), (post.title, post.content, post.published)
        )
        query_database.commit_changes_to_db()
    with open(
        path_builder(CURRENT_DIR, SQL_FOLDER, "last_created_post.sql"), "r"
    ) as query:
        query_database.execute_query(
            query.read(), (post.title, post.content, post.published)
        )
    return {"data": query_database.fetch_all_rows()}


@app.get("/posts/{id}")
def get_post_by_id(id: int) -> dict:
    """
    Endpoint to get a post by id.
    :param id: The id of the post to get.
    :return: The post with the given id in a dictionary under the 'data' key.
    """
    return find_post(id)


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int) -> Response:
    """
    Delete a post by its ID.

    Args:
        id (int): The ID of the post to delete.

    Returns:
        A 204 No Content HTTP status code if the post is found and deleted.
    """
    with open(
        path_builder(CURRENT_DIR, SQL_FOLDER, "delete_post_by_id.sql"), "r"
    ) as query:
        post = find_post(id)
        if post:
            query_database.execute_query(query.read(), (id,))
            query_database.commit_changes_to_db()
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
    post_id = find_post(id)
    if post_id:
        with open(
            path_builder(CURRENT_DIR, SQL_FOLDER, "update_post.sql"), "r"
        ) as query:
            query_database.execute_query(
                query.read(), (post.title, post.content, post.published, id)
            )
            query_database.commit_changes_to_db()
            return {"updated_post": find_post(id)}