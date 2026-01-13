from core.credit_applications.enums import ApplicationStatus
from core.exceptions import InvalidStateTransition


class RejectCreditApplication:
    """
    Use case representing the business decision to reject a credit application.
    """

    def __init__(self, repository):
        self.repository = repository

    def execute(
        self,
        application_id: str,
        reason: str | None = None,
    ):
        """
        Rejects a credit application.

        Args:
            application_id: ID of the application to reject
            reason: Optional business reason for rejection

        Raises:
            InvalidStateTransition: if the application cannot be rejected
        """
        application = self.repository.get(application_id)

        # Optional: store reason later (event, audit, entity field, etc.)
        application.change_status(ApplicationStatus.REJECTED)

        self.repository.save(application)

        return application
