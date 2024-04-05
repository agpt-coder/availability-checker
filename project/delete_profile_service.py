import prisma
import prisma.models
from pydantic import BaseModel


class DeleteUserProfileResponse(BaseModel):
    """
    This response model conveys the outcome of the delete operation, indicating success or providing error details.
    """

    success: bool
    message: str


async def delete_profile(userId: str) -> DeleteUserProfileResponse:
    """
    Deletes user profile.

    This function attempts to delete a user profile from the database based on the user's unique identifier.
    It involves removing the user's profile along with the user's related records due to cascading delete
    constraints set in the database schema.

    Args:
        userId (str): The unique identifier for the user whose profile is to be deleted.

    Returns:
        DeleteUserProfileResponse: This response model conveys the outcome of the delete operation,
        indicating success or providing error details.
    """
    try:
        await prisma.models.User.prisma().delete(where={"id": userId})
        return DeleteUserProfileResponse(
            success=True,
            message=f"User profile with ID {userId} has been successfully deleted.",
        )
    except Exception as error:
        return DeleteUserProfileResponse(
            success=False,
            message=f"Failed to delete user profile with ID {userId}. Error: {str(error)}",
        )
