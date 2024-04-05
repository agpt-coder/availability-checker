from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class AvailabilityStatus(BaseModel):
    """
    Enumerated type representing possible statuses of an availability slot such as AVAILABLE, UNAVAILABLE, IN_A_MEETING, ON_A_BREAK, EMERGENCY_ONLY, reflecting the db enum 'AvailabilityStatus'.
    """

    pass


class AvailabilitySlot(BaseModel):
    """
    This type represents the updated availability slot, mirroring the database model 'AvailabilitySlot' with fields for id, start time, end time, and status.
    """

    id: str
    userId: str
    startTime: datetime
    endTime: datetime
    status: AvailabilityStatus


class UpdateAvailabilitySlotResponse(BaseModel):
    """
    The response model for updating an availability slot, indicating the success or failure of the operation along with the updated availability slot details.
    """

    success: bool
    updatedSlotDetails: AvailabilitySlot


async def update_availability(
    slotId: str, startTime: datetime, endTime: datetime, status: AvailabilityStatus
) -> UpdateAvailabilitySlotResponse:
    """
    Updates an existing availability slot.

    Args:
        slotId (str): The unique identifier of the availability slot to be updated.
        startTime (datetime): The updated start time of the availability slot.
        endTime (datetime): The updated end time of the availability slot.
        status (AvailabilityStatus): The updated status of the availability slot, indicating its current condition (e.g., available, in a meeting, etc.).

    Returns:
        UpdateAvailabilitySlotResponse: The response model for updating an availability slot, indicating the success or failure of the operation along with the updated availability slot details.
    """
    try:
        updated_slot = await prisma.models.AvailabilitySlot.prisma().update(
            where={"id": slotId},
            data={"startTime": startTime, "endTime": endTime, "status": status},
        )
        updated_slot_details = AvailabilitySlot(
            id=updated_slot.id,
            userId=updated_slot.userId,
            startTime=updated_slot.startTime,
            endTime=updated_slot.endTime,
            status=updated_slot.status,
        )
        response = UpdateAvailabilitySlotResponse(
            success=True, updatedSlotDetails=updated_slot_details
        )
        return response
    except Exception as e:
        print(f"Error updating availability slot: {e}")
        return UpdateAvailabilitySlotResponse(success=False, updatedSlotDetails=None)
