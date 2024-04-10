from fastapi import status, APIRouter

router = APIRouter(tags=["Status endpoint"])


@router.get("/status", status_code=status.HTTP_200_OK)
def root() -> dict:
    return {"Message": "Server is running"}
