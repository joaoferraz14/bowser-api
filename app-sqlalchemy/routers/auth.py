from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..handlers.database_manager import get_db
from ..schemas.schemas import Token
from ..utils.utils import verify
from ..orm.models import User
from ..handlers.oauth2 import create_access_token

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> dict:
    """
    Authenticate a user and generate an access token for them.

    Args:
        user_credentials (OAuth2PasswordRequestForm): The user's credentials (username and password).
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the access token and token type.

    Raises:
        HTTPException: If authentication fails (e.g., invalid credentials).
    """
    # Query the User table to find the user by email
    user = db.query(User).filter(User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )

    # Verify the user's password
    if not verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )

    # Create an access token for the authenticated user
    access_token = create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
