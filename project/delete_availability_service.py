import prisma
import prisma.models
from pydantic import BaseModel


class DeleteAvailabilityResponse(BaseModel):
    """
    Response model for the deletion of an availability slot. Indicates success or failure and includes a message for context.
    """

    success: bool
    message: str


async def delete_availability(slotId: str, userId: str) -> DeleteAvailabilityResponse:
    """
    Removes an availability slot from the user's schedule.

    Args:
        slotId (str): The unique identifier of the availability slot to be deleted.
        userId (str): The unique identifier of the user requesting the deletion. This field is included to ensure that the deletion request is authenticated and authorized.

    Returns:
        DeleteAvailabilityResponse: Response model for the deletion of an availability slot. Indicates success or failure and includes a message for context.
    """
    slot = await prisma.models.AvailabilitySlot.prisma().find_unique(
        where={"id": slotId, "userId": userId}
    )
    if not slot:
        return DeleteAvailabilityResponse(
            success=False, message="Availability slot not found or unauthorized action."
        )
    await prisma.models.AvailabilitySlot.prisma().delete(where={"id": slotId})
    return DeleteAvailabilityResponse(
        success=True, message="Availability slot successfully deleted."
    )
