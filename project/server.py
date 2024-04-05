import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional

import prisma
import prisma.enums
import project.add_availability_service
import project.connect_calendar_service_service
import project.create_profile_service
import project.delete_availability_service
import project.delete_profile_service
import project.login_service
import project.logout_service
import project.register_service
import project.sync_calendar_events_service
import project.update_availability_service
import project.update_profile_service
import project.update_security_settings_service
import project.update_status_service
import project.view_profile_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="Availability Checker",
    lifespan=lifespan,
    description="To develop a function that returns the real-time availability of professionals, updating based on current activity or schedule, a system has been conceptualized using a tech stack involving Python, FastAPI, Prisma, and PostgreSQL. The requirements gathered indicate that the system should cater to professions such as healthcare professionals, emergency services personnel, IT support specialists, and customer service representatives, which necessitates a high degree of reliability and real-time responsiveness. \n\nThe proposed solution will utilize FastAPI to create RESTful API endpoints for managing user profiles, schedules, and availability updates. PostgreSQL, with Prisma as the ORM, will serve as the backend database, capable of storing and managing time-sensitive data, following best practices such as utilizing appropriate data types for time representation and implementing partitioning on time-based columns for optimized performance. \n\nFor real-time updates, the system will leverage WebSocket for bi-directional communication between the client and server. This will enable instant notification of availability changes triggered by various conditions such as acceptance of new projects, completion of tasks, or unexpected events like emergencies. On the server side, logical replication or triggers in PostgreSQL will be used to listen to change events and update the professional's availability status, which will then be broadcasted to relevant parties through WebSocket connections. \n\nThis approach ensures that the system can reliably track and update the availability status of professionals in real-time, enhancing the efficiency of emergency response, patient care, technical support, and customer service. It also provides a framework for scalability, allowing for the addition of more professions or customization of triggers for availability updates as needed.",
)


@app.post(
    "/status/update", response_model=project.update_status_service.UpdateStatusResponse
)
async def api_post_update_status(
    userId: str,
    newStatus: project.update_status_service.AvailabilityStatus,
    timestamp: Optional[datetime],
    reason: Optional[str],
) -> project.update_status_service.UpdateStatusResponse | Response:
    """
    Allows a user or system to update a professional's availability status.
    """
    try:
        res = project.update_status_service.update_status(
            userId, newStatus, timestamp, reason
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/user/schedule/availability",
    response_model=project.add_availability_service.AddAvailabilityResponse,
)
async def api_post_add_availability(
    userId: str,
    startTime: datetime,
    endTime: datetime,
    status: project.add_availability_service.AvailabilityStatus,
) -> project.add_availability_service.AddAvailabilityResponse | Response:
    """
    Adds a new availability slot to the user's schedule.
    """
    try:
        res = await project.add_availability_service.add_availability(
            userId, startTime, endTime, status
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/calendar/connect",
    response_model=project.connect_calendar_service_service.ConnectCalendarServiceOutput,
)
async def api_post_connect_calendar_service(
    userId: str, serviceProvider: str, authorizationToken: str
) -> project.connect_calendar_service_service.ConnectCalendarServiceOutput | Response:
    """
    Establishes a connection with an external calendar service for a user.
    """
    try:
        res = await project.connect_calendar_service_service.connect_calendar_service(
            userId, serviceProvider, authorizationToken
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/user/schedule/availability/{slotId}",
    response_model=project.delete_availability_service.DeleteAvailabilityResponse,
)
async def api_delete_delete_availability(
    slotId: str, userId: str
) -> project.delete_availability_service.DeleteAvailabilityResponse | Response:
    """
    Removes an availability slot from the user's schedule.
    """
    try:
        res = await project.delete_availability_service.delete_availability(
            slotId, userId
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/security/settings/update",
    response_model=project.update_security_settings_service.SecuritySettingsUpdateResponse,
)
async def api_put_update_security_settings(
    encryption_standards: str,
    communication_protocols: str,
    compliance_standards: str,
    admin_id: str,
) -> project.update_security_settings_service.SecuritySettingsUpdateResponse | Response:
    """
    Allows administrators to update security settings and policies of the system.
    """
    try:
        res = await project.update_security_settings_service.update_security_settings(
            encryption_standards,
            communication_protocols,
            compliance_standards,
            admin_id,
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/user/profile/{userId}",
    response_model=project.update_profile_service.UserProfileUpdatedResponse,
)
async def api_put_update_profile(
    userId: str,
    firstName: Optional[str],
    lastName: Optional[str],
    profession: Optional[str],
    email: Optional[str],
) -> project.update_profile_service.UserProfileUpdatedResponse | Response:
    """
    Updates the user profile information.
    """
    try:
        res = await project.update_profile_service.update_profile(
            userId, firstName, lastName, profession, email
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/user/schedule/availability/{slotId}",
    response_model=project.update_availability_service.UpdateAvailabilitySlotResponse,
)
async def api_put_update_availability(
    slotId: str,
    startTime: datetime,
    endTime: datetime,
    status: project.update_availability_service.AvailabilityStatus,
) -> project.update_availability_service.UpdateAvailabilitySlotResponse | Response:
    """
    Updates an existing availability slot.
    """
    try:
        res = await project.update_availability_service.update_availability(
            slotId, startTime, endTime, status
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/auth/logout", response_model=project.logout_service.LogoutResponse)
async def api_post_logout(
    session_token: str,
) -> project.logout_service.LogoutResponse | Response:
    """
    Invalidates the user's current session token.
    """
    try:
        res = await project.logout_service.logout(session_token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/auth/register", response_model=project.register_service.RegisterUserResponse
)
async def api_post_register(
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    profession: prisma.enums.Profession,
    oauth_credentials: Optional[project.register_service.OAuthCredentials],
) -> project.register_service.RegisterUserResponse | Response:
    """
    Registers a new user and initiates the authentication flow.
    """
    try:
        res = await project.register_service.register(
            email, password, first_name, last_name, profession, oauth_credentials
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/auth/login", response_model=project.login_service.LoginResponse)
async def api_post_login(
    email: str, password: str
) -> project.login_service.LoginResponse | Response:
    """
    Authenticates user and issues a session token.
    """
    try:
        res = await project.login_service.login(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/calendar/sync",
    response_model=project.sync_calendar_events_service.SyncCalendarEventsResponse,
)
async def api_post_sync_calendar_events(
    user_id: str, service_name: str, access_token: str, refresh_token: Optional[str]
) -> project.sync_calendar_events_service.SyncCalendarEventsResponse | Response:
    """
    Fetches and updates calendar events from the connected external calendar service.
    """
    try:
        res = await project.sync_calendar_events_service.sync_calendar_events(
            user_id, service_name, access_token, refresh_token
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/user/profile/{userId}",
    response_model=project.delete_profile_service.DeleteUserProfileResponse,
)
async def api_delete_delete_profile(
    userId: str,
) -> project.delete_profile_service.DeleteUserProfileResponse | Response:
    """
    Deletes user profile.
    """
    try:
        res = await project.delete_profile_service.delete_profile(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/user/profile", response_model=project.create_profile_service.UserProfileResponse
)
async def api_post_create_profile(
    userId: str,
    firstName: str,
    lastName: str,
    email: str,
    profession: prisma.enums.Profession,
) -> project.create_profile_service.UserProfileResponse | Response:
    """
    Creates a new user profile.
    """
    try:
        res = await project.create_profile_service.create_profile(
            userId, firstName, lastName, email, profession
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/user/profile/{userId}",
    response_model=project.view_profile_service.ViewProfileResponse,
)
async def api_get_view_profile(
    userId: str,
) -> project.view_profile_service.ViewProfileResponse | Response:
    """
    Retrieves the profile details of the user.
    """
    try:
        res = await project.view_profile_service.view_profile(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
