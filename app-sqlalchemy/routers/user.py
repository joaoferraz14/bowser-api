from typing import List
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from ..schemas.schemas import UserCreate, UserResponse
from ..handlers.database_manager import get_db
from ..utils.utils import hash
from ..orm import models
from ..handlers import oauth2

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    try:
        hashed_password = hash(user.password)
        user.password = hashed_password
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user {e}",
        )


@router.get("/{id}", response_model=UserResponse)
def get_user_by_id(
    id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(oauth2.get_current_user),
) -> UserResponse:
    db_user = db.query(models.User).filter(models.User.id == id).first()

    if db_user:
        return db_user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found"
    )


@router.get("/", response_model=List[UserResponse])
def get_users(
    db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)
) -> List[UserResponse]:
    return db.query(models.User).all()
