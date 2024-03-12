from fastapi import status, APIRouter

router = APIRouter(tags=["Status endpoint"])


@router.get("/status", status_code=status.HTTP_200_OK)
def root() -> dict:
    """
    Server status endpoint. Returns a status message.

    Returns:
        dict: A dictionary with a status message.
    """
    return {"Message": "Server is running"}
