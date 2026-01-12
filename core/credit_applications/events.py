from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from core.credit_applications.enums import Country, ApplicationStatus

@dataclass(frozen=True)
class CoreEvent:
    """
    Base class for all core events.
    """
    id: str
    occurred_at: datetime

    @staticmethod
    def new_event_id() -> str:
        return str(uuid4())

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
