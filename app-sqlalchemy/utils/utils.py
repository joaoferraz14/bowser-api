from passlib.context import CryptContext

# Initialize the password hashing context with the bcrypt scheme
pwd_context = CryptContext(schemes=["bcrypt"])


def hash(password: str) -> str:
    """
    Hash a password using the bcrypt scheme.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def verify(password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hashed password.

    Args:
        password (str): The plain-text password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    return pwd_context.verify(password, hashed_password)
