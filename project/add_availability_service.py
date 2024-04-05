from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from fastapi import HTTPException
from pydantic import BaseModel


class AvailabilityStatus(BaseModel):
    """
    Enumerated type representing possible statuses of an availability slot such as AVAILABLE, UNAVAILABLE, IN_A_MEETING, ON_A_BREAK, EMERGENCY_ONLY, reflecting the db enum 'AvailabilityStatus'.
    """

    pass


class AddAvailabilityResponse(BaseModel):
    """
    Provides feedback on the outcome of the add availability operation, including the details of the added slot or error messages.
    """

    message: str
    availabilitySlotId: Optional[str] = None
    error: Optional[str] = None


async def add_availability(
    userId: str, startTime: datetime, endTime: datetime, status: AvailabilityStatus
) -> AddAvailabilityResponse:
    """
    Adds a new availability slot to the user's schedule.

    Args:
        userId (str): The ID of the user for whom the availability slot is being added.
        startTime (datetime): The start time of the availability slot, in an appropriate datetime format.
        endTime (datetime): The end time of the availability slot, also in an appropriate datetime format.
        status (AvailabilityStatus): The availability status for the slot, referencing predefined values in the 'AvailabilityStatus' enum.

    Returns:
        AddAvailabilityResponse: Provides feedback on the outcome of the add availability operation, including the details of the added slot or error messages.

    Raises:
        HTTPException: If the user does not exist, or the availability slot times are invalid.
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": userId})
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {userId} not found.")
    if startTime >= endTime:
        return AddAvailabilityResponse(
            message="Failure", error="Start time must be before end time."
        )
    new_slot = await prisma.models.AvailabilitySlot.prisma().create(
        data={
            "userId": userId,
            "startTime": startTime,
            "endTime": endTime,
            "status": status,
        }
    )
    return AddAvailabilityResponse(message="Success", availabilitySlotId=new_slot.id)
