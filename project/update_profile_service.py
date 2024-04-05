from typing import Dict, Optional

from pydantic import BaseModel


class UserProfileUpdatedResponse(BaseModel):
    """
    The response model confirming the update of a user profile with a message and the updated fields.
    """

    success: bool
    message: str
    updatedFields: Dict[str, str]


async def update_profile(
    userId: str,
    firstName: Optional[str],
    lastName: Optional[str],
    profession: Optional[str],
    email: Optional[str],
) -> UserProfileUpdatedResponse:
    """
    Updates the user profile information.

    Args:
    userId (str): The unique identifier of the user whose profile is to be updated. This is a path parameter.
    firstName (Optional[str]): The user's updated first name. Optional for allowing partial updates.
    lastName (Optional[str]): The user's updated last name. Optional.
    profession (Optional[str]): The user's updated profession. Optional.
    email (Optional[str]): The user's updated email address. Optional.

    Returns:
    UserProfileUpdatedResponse: The response model confirming the update of a user profile with a message and the updated fields.
    """
    import prisma.models

    updated_fields = {}
    user = await prisma.models.User.prisma().find_unique(where={"id": userId})
    if user is None:
        return UserProfileUpdatedResponse(
            success=False, message="User not found", updatedFields={}
        )
    profile_data = {}
    if firstName is not None:
        profile_data["firstName"] = firstName
        updated_fields["firstName"] = firstName
    if lastName is not None:
        profile_data["lastName"] = lastName
        updated_fields["lastName"] = lastName
    if profession is not None:
        profile_data["profession"] = profession
        updated_fields["profession"] = profession
    if email is not None:
        user_update = await prisma.models.User.prisma().update(
            where={"id": userId}, data={"email": email}
        )
        updated_fields["email"] = email
    if profile_data:
        await prisma.models.Profile.prisma().update(
            where={"userId": userId}, data=profile_data
        )
    return UserProfileUpdatedResponse(
        success=True,
        message="Profile updated successfully",
        updatedFields=updated_fields,
    )
