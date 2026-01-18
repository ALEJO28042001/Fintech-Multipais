from typing import List, Optional

from core.credit_applications.repository import (
    CreditApplicationRepository,
)


class ListCreditApplications:
    def __init__(self, repository: CreditApplicationRepository):
        self.repository = repository

    def execute(
        self,
        country: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[dict]:
        applications = self.repository.list(
            country=country,
            status=status,
        )

        return [
            {
                "id": app.id,
                "country": app.country,
                "status": app.status.value,
                "requested_amount": app.requested_amount.amount,
                "created_at": app.created_at,
            }
            for app in applications
        ]
