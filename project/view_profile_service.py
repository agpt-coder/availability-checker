from datetime import datetime

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class ViewProfileResponse(BaseModel):
    """
    Model representing the detailed profile information of a user including personal and professional data.
    """

    id: str
    firstName: str
    lastName: str
    profession: prisma.enums.Profession
    createdAt: datetime
    updatedAt: datetime


async def view_profile(userId: str) -> ViewProfileResponse:
    """
    Retrieves the profile details of the user.

    Args:
        userId (str): The unique identifier of the user whose profile details are to be retrieved. It's extracted from the request path.

    Returns:
        ViewProfileResponse: Model representing the detailed profile information of a user including personal and professional data.

    Example:
        userId = "example-uuid"
        userProfile = await view_profile(userId)
        print(userProfile)
        > ViewProfileResponse(id="example-uuid", firstName="John", lastName="Doe", profession=prisma.enums.Profession.HEALTHCARE_PROFESSIONAL,
          createdAt=datetime(2022, 1, 1), updatedAt=datetime(2022, 1, 2))
    """
    profile = await prisma.models.Profile.prisma().find_unique(
        where={"userId": userId}, include={"User": True}
    )
    if profile is None:
        pass
    response = ViewProfileResponse(
        id=profile.id,
        firstName=profile.firstName,
        lastName=profile.lastName,
        profession=profile.profession,
        createdAt=profile.User.createdAt,
        updatedAt=profile.User.updatedAt,
    )
    return response
