from core.credit_applications.enums import ApplicationStatus
from core.exceptions import CoreValidationError


class ApproveCreditApplication:

    def __init__(self, repository):
        self.repository = repository

    def execute(self, application_id: str):
        application = self.repository.get(application_id)

        if application.status not in {
            ApplicationStatus.VALIDATED,
            ApplicationStatus.UNDER_REVIEW,
        }:
            raise CoreValidationError(
                "Application cannot be approved in current state"
            )

        # Business precondition (not a state transition)
        if not application.bank_snapshot:
            raise CoreValidationError(
                "Cannot approve application without bank snapshot"
            )

        # Core-enforced transition
        application.change_status(ApplicationStatus.APPROVED)

        self.repository.save(application)

        return application
