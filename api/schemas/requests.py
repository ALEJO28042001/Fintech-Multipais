from pydantic import BaseModel
from decimal import Decimal


class CreateCreditApplicationRequest(BaseModel):
    country: str
    full_name: str
    document_value: str
    requested_amount: Decimal
    monthly_income: Decimal
    document_type: str
    currency: str