from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime, UTC
from core.credit_applications.enums import ApplicationStatus

class CreditApplicationResponse(BaseModel):
    id: str
    country: str
    status: ApplicationStatus
    requested_amount: Decimal
    created_at: datetime.now(UTC)
    bank_snapshot: any
