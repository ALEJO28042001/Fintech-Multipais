from core.countries.base import CountryPolicy
from core.credit_applications.enums import DocumentType
from core.exceptions import CoreValidationError
import re
from decimal import Decimal

class SpainPolicy(CountryPolicy):

    """
    Country-specific business rules for Spain (SP).
    """

    REVIEW_THRESHOLD = Decimal("10000")

    def validate(self, application):
        self._validate_document_type(application.applicant.document.document_type)
        self._validate_document_format(application.applicant.document.value)

    def _validate_document_type(self, document_type):
        if document_type != DocumentType.DNI:
            raise CoreValidationError(
                "Spain requires DNI document"
            )

    def _validate_document_format(self, dni: str) -> None:
        if not re.match(r"^[0-9]{8}[A-Z]$", dni):
            raise CoreValidationError("Invalid DNI format")

    def requires_additional_review(self, application) -> bool:
        return (
            application.requested_amount.amount
            > self.REVIEW_THRESHOLD
        )
