from ..adapters.database_connection import SessionLocal
from sqlalchemy.orm import Session


def get_db() -> Session:
    """
    Get a database session.

    Yields:
        Session: A SQLAlchemy database session.

    Yields:
        Session: A SQLAlchemy database session.

    Example:
        Usage in a FastAPI endpoint:
        ```python
        def some_endpoint(db: Session = Depends(get_db)):
            # Your code that uses the database session
            pass
        ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
