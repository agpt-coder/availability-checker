from datetime import datetime, timedelta
from typing import Union

import prisma
import prisma.models
from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel


class LoginResponse(BaseModel):
    """
    This model represents the response returned upon a successful login, including the session token for subsequent requests.
    """

    session_token: str
    expires_at: datetime


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "a very secretive secret key"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(
    data: dict, expires_delta: Union[timedelta, None] = None
) -> str:
    """
    Generates an access token with given data payload and expiration.

    Args:
        data (dict): Data payload to include in the token.
        expires_delta (Union[timedelta, None]): Expiry duration for the token. If None, defaults to configured expiry minutes.

    Returns:
        str: Generated access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    """
    Verifies if a plaintext password matches a given hash.

    Args:
        plain_password: Non-hashed password input for verification.
        hashed_password: Previously hashed password for comparison.

    Returns:
        bool: True if passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


async def login(email: str, password: str) -> LoginResponse:
    """
    Authenticates user and issues a session token.

    Checks the provided email and password against the database,
    generates a JWT token for authenticated users.

    Args:
        email (str): The user's email address used for login.
        password (str): The user's password. This will be securely handled and never stored in plain text.

    Returns:
        LoginResponse: This model represents the response returned upon a successful login, including the session token for subsequent requests.

    Raises:
        HTTPException: With status code 401 for unauthorized access attempts.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if not user or not verify_password(password, user.hashedPassword):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return LoginResponse(
        session_token=access_token, expires_at=datetime.utcnow() + access_token_expires
    )
