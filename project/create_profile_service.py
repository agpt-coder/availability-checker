from datetime import datetime

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class UserProfileResponse(BaseModel):
    """
    Model representing the successfully created user profile, returning basic and professional information.
    """

    profileId: str
    userId: str
    createdAt: datetime
    profession: str
    status: str


async def create_profile(
    userId: str,
    firstName: str,
    lastName: str,
    email: str,
    profession: prisma.enums.Profession,
) -> UserProfileResponse:
    """
    Creates a new user profile.

    This function creates a new profile for a user in the system. It includes basic user information and their professional designation.

    Args:
        userId (str): The unique identifier of the user for whom the profile is created. This could be the same as the User model id.
        firstName (str): User's first name.
        lastName (str): User's last name.
        email (str): User's email address. This should be unique and hence could be validated against existing profiles.
        profession (prisma.enums.Profession): The profession of the user as defined by the available enums. This helps in categorizing professional expertise.

    Returns:
        UserProfileResponse: Model representing the successfully created user profile, returning basic and professional information.

    Raises:
        ValueError: If the email address is already associated with another user.
    """
    existing_profile = await prisma.models.Profile.prisma().find_first(
        where={"User": {"email": email}}
    )
    if existing_profile:
        raise ValueError("The email address is already associated with another user.")
    new_profile = await prisma.models.Profile.prisma().create(
        data={
            "firstName": firstName,
            "lastName": lastName,
            "profession": profession,
            "User": {"connect": {"id": userId}},
        }
    )
    response = UserProfileResponse(
        profileId=new_profile.id,
        userId=userId,
        createdAt=new_profile.createdAt,
        profession=new_profile.profession.value,
        status="Success",
    )
    return response
