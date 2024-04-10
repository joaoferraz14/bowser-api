from typing import Dict, List, Optional
from fastapi import HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from ..schemas.schemas import CreatePost, UpdatePost, PostResponse
from ..handlers.database_manager import get_db
from ..orm import models
from ..handlers import oauth2

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[PostResponse])
def get_posts(
    db: Session = Depends(get_db),
    user_id: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
) -> List[PostResponse]:
    return (
        db.query(models.Post)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(
    post: CreatePost,
    db: Session = Depends(get_db),
    user_id: int = Depends(oauth2.get_current_user),
) -> PostResponse:
    try:
        db_post = models.Post(owner_id=user_id.id, **post.dict())
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


@router.get("/{id}", response_model=PostResponse)
def get_post_by_id(
    id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(oauth2.get_current_user),
) -> PostResponse:
    db_post = db.query(models.Post).filter(models.Post.id == id).first()
    if db_post:
        return db_post
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found"
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(oauth2.get_current_user),
) -> Response:
    db_post = db.query(models.Post).get(id)

    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} not found"
        )

    if int(db_post.owner_id) != int(user_id.id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your user does not own the post. Can't be deleted",
        )

    db.delete(db_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=PostResponse)
def update_post(
    id: int,
    post: UpdatePost,
    db: Session = Depends(get_db),
    user_id: int = Depends(oauth2.get_current_user),
) -> PostResponse:
    db_post_query = db.query(models.Post).filter(models.Post.id == id)
    post_data = db_post_query.first()

    if int(post_data.owner_id) != int(user_id.id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your user does not own the post. Can't be updated",
        )

    if post_data:
        db_post_query.update(post.dict(), synchronize_session=False)
        db.commit()
        return db_post_query.first()
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} not found"
    )
