from jose import JWTError, jwt
from datetime import datetime, timedelta
from ..schemas.schemas import TokenData
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from ..utils.config import settings


oaut2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict) -> str:
    """
    Create an access token with the provided data.

    Args:
        data (dict): The data to be encoded into the token.

    Returns:
        str: The encoded JWT access token.

    Example:
        access_token = create_access_token({"user_id": "example_user_id"})
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update(
        {"exp": expire}
    )  # needs to be exp because it's the key expected in minutes for the token to expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    """
    Verify and decode an access token.

    Args:
        token (str): The access token to be verified and decoded.
        credentials_exception: An HTTPException to raise if token verification fails.

    Returns:
        TokenData: The decoded token data.

    Raises:
        HTTPException: If token verification fails.

    Example:
        token_data = verify_access_token(token, credentials_exception)
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oaut2_scheme)) -> TokenData:
    """
    Get the current user based on the access token.

    Args:
        token (str): The access token.

    Returns:
        TokenData: The user's token data.

    Raises:
        HTTPException: If the token is invalid.

    Example:
        current_user = get_current_user(token)
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "bearer"},
    )
    return verify_access_token(token, credentials_exception)
