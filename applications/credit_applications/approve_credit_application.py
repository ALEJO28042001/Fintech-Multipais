from core.credit_applications.enums import ApplicationStatus
from core.exceptions import CoreValidationError


class ApproveCreditApplication:
    """
    Approves a credit application once all business preconditions are met.
    """

    def __init__(self, repository):
        self.repository = repository

    def execute(self, application_id: str):
        application = self.repository.get(application_id)
        print(application)
        # Business precondition (not a state transition)
        # if not application.bank_snapshot:
        #     raise CoreValidationError(
        #         "Cannot approve application without bank snapshot"
        #     )

        # Domain-enforced transition
        application.change_status(ApplicationStatus.APPROVED)

        self.repository.save(application)

        # Side effects (out of domain)

        return application
