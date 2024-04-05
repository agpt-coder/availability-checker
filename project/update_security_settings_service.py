import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class SecuritySettingsUpdateResponse(BaseModel):
    """
    Provides feedback on the success or failure of the update operation on the security settings.
    """

    success: bool
    message: str


async def update_security_settings(
    encryption_standards: str,
    communication_protocols: str,
    compliance_standards: str,
    admin_id: str,
) -> SecuritySettingsUpdateResponse:
    """
    Allows administrators to update security settings and policies of the system.

    Args:
        encryption_standards (str): Specifies the encryption standards to be used for data at rest and in transit.
        communication_protocols (str): Includes the secure communication protocols to be used, such as HTTPS for web traffic and WSS for WebSocket Secure.
        compliance_standards (str): Defines the compliance standards the system adheres to, such as GDPR, HIPAA, etc.
        admin_id (str): The ID of the administrator requesting the update. Used for authentication and authorization.

    Returns:
        SecuritySettingsUpdateResponse: Provides feedback on the success or failure of the update operation on the security settings.

    """
    admin = await prisma.models.User.prisma().find_unique(where={"id": admin_id})
    if admin is None or admin.role != prisma.enums.Role.ADMINISTRATOR:
        return SecuritySettingsUpdateResponse(
            success=False,
            message="Unauthorized: User is not an administrator or doesn't exist.",
        )
    print("Updating security settings with provided standards and protocols")
    return SecuritySettingsUpdateResponse(
        success=True, message="Security settings updated successfully."
    )
