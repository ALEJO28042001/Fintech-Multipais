from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4
from decimal import Decimal
from core.credit_applications.events import CoreEvent


from core.credit_applications.enums import (
    Country,
    ApplicationStatus,
)
from core.credit_applications.value_objects import (
    Money,
    Income,
    Document,
)
from core.exceptions import InvalidStateTransition

@dataclass
class Applicant:
    """
    Represents the person applying for credit.
    This entity has no independent lifecycle outside CreditApplication.
    """
    full_name: str
    document: Document

@dataclass(frozen=True)
class BankSnapshot:
    """
    Immutable snapshot of external banking data used for evaluation.
    """
    provider: str
    payload: dict
    fetched_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

@dataclass
class CreditApplication:
    """
    Aggregate Root for the credit application domain.
    """
    id: str
    country: Country
    applicant: Applicant
    requested_amount: Money
    monthly_income: Income
    status: ApplicationStatus = field(
            default=ApplicationStatus.CREATED,
            init=False
        )

    _events: list[CoreEvent] = field(default_factory=list, init=False)


    def change_status(self, new_status: ApplicationStatus) -> None:
        """
        The only valid way to change application status.
        """
        if not self._can_transition(new_status):
            raise InvalidStateTransition(
                f"Cannot transition from {self.status} to {new_status}"
            )
        self.status = new_status
        
    def _can_transition(self, new_status: ApplicationStatus) -> bool:
        transitions = {
            ApplicationStatus.CREATED: {
                ApplicationStatus.VALIDATED,
                ApplicationStatus.REJECTED,
            },
            ApplicationStatus.VALIDATED: {
                ApplicationStatus.UNDER_REVIEW,
                ApplicationStatus.APPROVED,
                ApplicationStatus.REJECTED,
            },
            ApplicationStatus.UNDER_REVIEW: {
                ApplicationStatus.APPROVED,
                ApplicationStatus.REJECTED,
            },
        }
        return new_status in transitions.get(self.status, set())
