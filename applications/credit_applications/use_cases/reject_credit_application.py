from core.credit_applications.enums import ApplicationStatus
from core.exceptions import CoreValidationError


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
        application = self.repository.get(application_id)

        # Business guard (intent-level)
        if application.status in {
            ApplicationStatus.APPROVED,
            ApplicationStatus.REJECTED,
        }:
            raise CoreValidationError(
                f"Application cannot be rejected in state {application.status}"
            )

        # Core-enforced transition
        application.change_status(ApplicationStatus.REJECTED)

        # Optional: store reason later (audit / event)
        # application.rejection_reason = reason

        self.repository.save(application)
        return application
