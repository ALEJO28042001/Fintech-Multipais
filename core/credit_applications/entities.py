from dataclasses import dataclass, field
from datetime import datetime,timezone
from uuid import uuid4
from decimal import Decimal
from typing import Optional

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

@dataclass(frozen=True)
class ApplicationStatusChanged(CoreEvent):
    application_id: str
    previous_status: ApplicationStatus
    new_status: ApplicationStatus

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
    bank_snapshot: BankSnapshot | None = field(default=None, init=False)

    status: ApplicationStatus = field(
            default=ApplicationStatus.CREATED,
            init=False
        )

    _events: list[CoreEvent] = field(default_factory=list, init=False)

    def attach_bank_snapshot(self, snapshot: BankSnapshot) -> None:
        if self.bank_snapshot is not None:
            raise CoreError("Bank snapshot already attached")

        self.bank_snapshot = snapshot

    def change_status(self, new_status: ApplicationStatus) -> None:
        """
        The only valid way to change application status.
        """
        if not self._can_transition(new_status):
            raise InvalidStateTransition(
                f"Core Error: Cannot transition from {self.status} to {new_status}"
            )
        
        self._events.append(
            ApplicationStatusChanged(
                id=str(uuid4()),
                occurred_at=datetime.now(timezone.utc),
                application_id=self.id,
                previous_status=self.status,
                new_status=new_status,
            )
        )


        self.status = new_status
        
        
    def _can_transition(self, new_status: ApplicationStatus) -> bool:
        transitions = {
            ApplicationStatus.CREATED: {
                ApplicationStatus.VALIDATED,
                ApplicationStatus.UNDER_REVIEW,
                ApplicationStatus.REJECTED,
            },
            ApplicationStatus.VALIDATED: {
                # ApplicationStatus.UNDER_REVIEW,
                ApplicationStatus.APPROVED,
                ApplicationStatus.REJECTED,
            },
            ApplicationStatus.UNDER_REVIEW: {
                # ApplicationStatus.APPROVED,
                ApplicationStatus.REJECTED,
                ApplicationStatus.VALIDATED,
            },
        }
        return new_status in transitions.get(self.status, set())

    def pull_events(self) -> list[CoreEvent]:
        events = self._events[:]
        self._events.clear()
        return events


