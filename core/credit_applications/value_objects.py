from dataclasses import dataclass
from decimal import Decimal
from core.exceptions import ValidationError
from core.credit_applications.enums import Currency
from core.credit_applications.enums import DocumentType, Country

@dataclass(frozen=True)
class Money:
    """
    Represents a monetary value.
    """
    amount: Decimal
    currency: Currency

    def __post_init__(self):
        if self.amount <=  Decimal("0"):
            raise ValidationError("Core Error: Amount must be greater than zero")

@dataclass(frozen=True)
class Income:
    """
    Monthly income of the applicant.
    """
    monthly_amount: Decimal
    currency: Currency

    def __post_init__(self):
        if self.monthly_amount <= Decimal("0"):
            raise ValidationError("Core Error: Monthly income must be greater than zero")

@dataclass(frozen=True)
class Document:
    """
    Identification document.
    Validation rules depend on the country.
    """
    document_type: DocumentType
    value: str
    country: Country

    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValidationError("Core Error: Document value cannot be empty")

    def masked(self) -> str:
        """
        Masks sensitive document data.
        """
        return f"{self.value[:3]}****{self.value[-2:]}"
