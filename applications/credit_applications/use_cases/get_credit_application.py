from core.credit_applications.repository import CreditApplicationRepository

from core.exceptions import NotFoundError


class GetCreditApplication:
    """
    Retrieves a single credit application by ID.

    Application layer responsibility:
    - Coordinate repository access
    - Translate None → domain error
    """

    def __init__(self, repository: CreditApplicationRepository):
        self.repository = repository

    def execute(self, application_id: str) -> dict:
        application = self.repository.get(application_id)

        if application is None:
            raise NotFoundError(f"Credit application {application_id} not found")

        return application
