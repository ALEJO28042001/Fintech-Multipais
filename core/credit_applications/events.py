from dataclasses import dataclass
from datetime import datetime,timezone
from uuid import uuid4

from core.credit_applications.enums import Country, ApplicationStatus

@dataclass(frozen=True)
class CoreEvent:
    id: str
    occurred_at: datetime

    @staticmethod
    def new():
        return {
            "id": str(uuid4()),
            "occurred_at": datetime.now(timezone.utc),
        }

"""
Specific Events for Application states
"""
@dataclass(frozen=True)
class CreditApplicationCreated(CoreEvent):
    application_id: str
    country: Country

@dataclass(frozen=True)
class CreditApplicationValidated(CoreEvent):
    application_id: str

@dataclass(frozen=True)
class CreditApplicationRejected(CoreEvent):
    application_id: str
    reason: str

@dataclass(frozen=True)
class CreditApplicationApproved(CoreEvent):
    application_id: str


@dataclass(frozen=True)
class BankSnapshotAttached(CoreEvent):
    """
    Event for returning bank info during the application.
    """
    application_id: str
    provider: str
