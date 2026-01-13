from core.credit_applications.enums import ApplicationStatus
from core.credit_applications.entities import CreditApplication
from core.exceptions import InvalidStateTransition


class UpdateCreditApplicationState:
    """
    Use case responsible only for changing the state of a credit application.
    """

    def __init__(self, repository):
        self.repository = repository

    def execute(
        self,
        application_id: str,
        new_status: ApplicationStatus,
    ) -> CreditApplication:
        """
        Updates the application state if the transition is valid.

        Raises:
            InvalidStateTransition: if the transition is not allowed
        """
        application = self.repository.get(application_id)

        application.change_status(new_status)

        self.repository.save(application)

        return application
