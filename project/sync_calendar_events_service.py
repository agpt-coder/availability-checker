from datetime import datetime
from typing import Optional

import httpx
import prisma
import prisma.models
from pydantic import BaseModel


class SyncCalendarEventsResponse(BaseModel):
    """
    The response after attempting to synchronize calendar events with an external service. Includes the status of the sync process and any messages regarding success or failure.
    """

    success: bool
    message: str
    synced_events_count: int


async def fetch_external_calendar_events(
    service_name: str, access_token: str
) -> Optional[list]:
    """
    Fetches calendar events from an external calendar service.

    This is a placeholder for the API call implementation to fetch events from the specified service.
    It needs to be tailored to the service being synchronized (e.g. Google Calendar, Microsoft Outlook).

    Args:
        service_name (str): The name of the external calendar service.
        access_token (str): The access token required for API requests to the service.

    Returns:
        Optional[list]: A list of event dictionaries fetched from the external service or None if the request fails.
    """
    url = f"https://{service_name}.com/api/events"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            events = response.json()
            return events
    except Exception as e:
        print(f"Error fetching calendar events: {str(e)}")
        return None


async def store_calendar_events(user_id: str, events: list) -> int:
    """
    Stores fetched calendar events in the database.

    Args:
        user_id (str): The user ID for whom the events are to be stored.
        events (list): A list of event dictionaries to be stored.

    Returns:
        int: The number of events successfully stored.
    """
    count = 0
    for event in events:
        await prisma.models.CalendarEvent.prisma().create(
            data={
                "userId": user_id,
                "externalId": event["externalId"],
                "summary": event["summary"],
                "description": event.get("description", ""),
                "start": datetime.fromisoformat(event["start"]),
                "end": datetime.fromisoformat(event["end"]),
                "location": event.get("location", ""),
                "url": event.get("url", ""),
                "syncedAt": datetime.now(),
            }
        )
        count += 1
    return count


async def sync_calendar_events(
    user_id: str, service_name: str, access_token: str, refresh_token: Optional[str]
) -> SyncCalendarEventsResponse:
    """
    Fetches and updates calendar events from the connected external calendar service.

    This function synchronizes a user's calendar events with their external service of choice.

    Args:
        user_id (str): The unique identifier of the user whose calendar events are to be synchronized.
        service_name (str): The name of the external calendar service.
        access_token (str): The access token required for authenticating API requests.
        refresh_token (Optional[str]): Optional refresh token.

    Returns:
        SyncCalendarEventsResponse: The response after attempting to synchronize.
    """
    events = await fetch_external_calendar_events(service_name, access_token)
    if not events:
        return SyncCalendarEventsResponse(
            success=False,
            message="Failed to fetch events from external service.",
            synced_events_count=0,
        )
    events_count = await store_calendar_events(user_id, events)
    if events_count > 0:
        return SyncCalendarEventsResponse(
            success=True,
            message="Events synchronized successfully.",
            synced_events_count=events_count,
        )
    else:
        return SyncCalendarEventsResponse(
            success=False,
            message="No new events to synchronize.",
            synced_events_count=0,
        )
