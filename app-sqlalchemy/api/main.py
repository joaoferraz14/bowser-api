from typing import Dict, List
from fastapi import FastAPI, HTTPException, status, Response, Depends
from sqlalchemy.orm import Session
from ..schemas.schemas import CreatePost, UpdatePost, PostResponse, UserCreate, UserResponse
from ..handlers.database_manager import get_db
from passlib.context import CryptContext
from dotenv import load_dotenv
from ..orm import models
from ..adapters.database_connection import engine

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], depecrated="auto")
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/status", status_code=status.HTTP_200_OK)
def root() -> dict:
    """Server status endpoint. Returns a status message."""
    return {"Message": "Server is running"}


@app.get("/posts", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)) -> dict:
    """
    Endpoint to get all the posts.
    :param db: Database session dependency.
    :return: All posts in a dictionary under the 'data' key.
    """
    return db.query(models.Post).all()


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: CreatePost, db: Session = Depends(get_db)) -> dict:
    """
    Endpoint to create a new post.
    :param post: Post input model.
    :param db: Database session dependency.
    :return: The newly created post in a dictionary under the 'data' key.
    """
    try:
        db_post = models.Post(**post.dict())
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create post {e}",
        )


@app.get("/posts/{id}", response_model=PostResponse)
def get_post_by_id(id: int, db: Session = Depends(get_db)) -> dict:
    """
    Endpoint to get a post by id.
    :param id: The id of the post to get.
    :param db: Database session dependency.
    :return: The post with the given id in a dictionary under the 'data' key.
    """
    db_post = db.query(models.Post).filter(models.Post.id==id).first()
    try:
        if db_post:
            return db_post.__dict__
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id: {id} not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to retrieve post - internal server error'
        )


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)) -> Response:
    """
    Delete a post by its ID.

    Args:
        id (int): The ID of the post to delete.
        db: Database session dependency.

    Returns:
        A 204 No Content HTTP status code if the post is found and deleted.
    """
    db_post = db.query(models.Post).get(id)
    if db_post:
        db.delete(db_post)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with ID {id} not found"
    )


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=PostResponse)
def update_post(id: int, post: UpdatePost, db: Session = Depends(get_db)) -> Dict[str, object]:
    """
    Update a post by its ID.

    Args:
        id (int): The ID of the post to update.
        post (Post): The new post data.
        db: Database session dependency.

    Returns:
        A dictionary with a response message and the updated data if the post is found and updated.
    """
    db_post_query = db.query(models.Post).filter(models.Post.id==id)
    post_data = db_post_query.first()
    if post_data:
        db_post_query.update(post.dict(), synchronize_session=False)
        db.commit()
        return db_post_query.first().__dict__
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with ID {id} not found"
    )

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:

        
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create post {e}",
        )
