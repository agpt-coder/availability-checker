from typing import Optional

import bcrypt
import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class OAuthCredentials(BaseModel):
    """
    Credentials for OAuth flow to integrate external calendar services.
    """

    service_provider: str
    access_token: str


class RegisterUserResponse(BaseModel):
    """
    A model representing the outcome of the registration process. It includes a status message and basic user information if the registration is successful.
    """

    success: bool
    message: str
    user_id: Optional[str] = None
    email: Optional[str] = None


async def register(
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    profession: prisma.enums.Profession,
    oauth_credentials: Optional[OAuthCredentials],
) -> RegisterUserResponse:
    """
    Registers a new user and initiates the authentication flow.

    Args:
    email (str): The email address of the new user, to be used as the primary method of contact and identification.
    password (str): The chosen password for the new user, which will be securely hashed before storage.
    first_name (str): The first name of the user.
    last_name (str): The last name of the user.
    profession (Profession): The profession of the user, chosen from a predefined list of roles.
    oauth_credentials (Optional[OAuthCredentials]): Optional OAuth credentials for calendar integration, if the user wishes to connect their external calendar during registration.

    Returns:
    RegisterUserResponse: A model representing the outcome of the registration process. It includes a status message and basic user information if the registration is successful.
    """
    existing_user = await prisma.models.User.prisma().find_unique(
        where={"email": email}
    )
    if existing_user:
        return RegisterUserResponse(
            success=False, message="Email already in use", email=email
        )
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )
    user = await prisma.models.User.prisma().create(
        data={
            "email": email,
            "hashedPassword": hashed_password,
            "profiles": {
                "create": {
                    "firstName": first_name,
                    "lastName": last_name,
                    "profession": profession,
                }
            },
        }
    )
    if oauth_credentials:
        pass
    return RegisterUserResponse(
        success=True,
        message="Registration successful",
        user_id=user.id,
        email=user.email,
    )
