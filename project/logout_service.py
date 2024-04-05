import prisma
import prisma.models
from pydantic import BaseModel


class LogoutResponse(BaseModel):
    """
    This response model conveys the outcome of the logout attempt, indicating success or providing error information.
    """

    success: bool
    message: str


async def logout(session_token: str) -> LogoutResponse:
    """
    Invalidates the user's current session token.

    This function looks up the session matching the provided token in the database and sets its valid field to False,
    effectively invalidating the session. It handles the case where the session token is not found or already invalid.

    Args:
        session_token (str): The session token issued to the user upon log in, used to authenticate the logout request.

    Returns:
        LogoutResponse: This response model conveys the outcome of the logout attempt, indicating success or providing error information.

    Example:
        logout_response = logout("some_valid_session_token")
        if logout_response.success:
            print(logout_response.message)  # "Successfully logged out."
        else:
            print(logout_response.message)  # "Failed to log out. Please try again."
    """
    session = await prisma.models.Session.prisma().find_unique(
        where={"refreshToken": session_token}
    )
    if session is None or not session.valid:
        return LogoutResponse(
            success=False, message="Session token is invalid or already logged out."
        )
    await prisma.models.Session.prisma().update(
        where={"refreshToken": session_token}, data={"valid": False}
    )
    return LogoutResponse(success=True, message="Successfully logged out.")
