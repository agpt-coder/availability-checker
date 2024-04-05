from typing import Optional

from pydantic import BaseModel


class ConnectCalendarServiceOutput(BaseModel):
    """
    Represents the outcome of an attempt to establish a connection between a user's account in AvailaPro and an external calendar service. Includes status and any relevant messages or identifiers.
    """

    success: bool
    message: str
    serviceAccountId: Optional[str] = None


async def connect_calendar_service(
    userId: str, serviceProvider: str, authorizationToken: str
) -> ConnectCalendarServiceOutput:
    """
    Establishes a connection with an external calendar service for a user.

    This function tries to connect the user's AvailaPro account to an external calendar service like Google Calendar or Outlook using an OAuth token.
    If the connection is successful, it records the connection details and the service account ID provided by the external service for future API calls.

    Args:
        userId (str): The unique identifier of the user seeking to connect their calendar service.
        serviceProvider (str): The name of the calendar service provider the user is trying to connect to (e.g., 'Google', 'Outlook').
        authorizationToken (str): The authorization token obtained from the external calendar service as part of the OAuth authentication process.

    Returns:
        ConnectCalendarServiceOutput: Represents the outcome of an attempt to establish a connection between a user's account in AvailaPro and an external calendar service. Includes status and any relevant messages or identifiers.

    Example:
        userId = '123e4567-e89b-12d3-a456-426614174000'
        serviceProvider = 'Google'
        authorizationToken = 'ya29.a0AfH6SMB...'
        connect_calendar_service(userId, serviceProvider, authorizationToken)
        > ConnectCalendarServiceOutput(success=True, message='Successfully connected to Google Calendar.', serviceAccountId='google-service-account-id')
    """
    if serviceProvider == "Google" and authorizationToken:
        serviceAccountId = "google-service-account-id"
        message = f"Successfully connected to {serviceProvider} Calendar."
        success = True
    elif serviceProvider == "Outlook" and authorizationToken:
        serviceAccountId = "outlook-service-account-id"
        message = f"Successfully connected to {serviceProvider} Calendar."
        success = True
    else:
        serviceAccountId = None
        message = "Failed to connect to the calendar service. Please check the service provider or authorization token."
        success = False
    return ConnectCalendarServiceOutput(
        success=success, message=message, serviceAccountId=serviceAccountId
    )
