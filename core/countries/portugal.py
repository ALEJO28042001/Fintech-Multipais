import re
from decimal import Decimal
from core.countries.base import CountryPolicy
from core.credit_applications.enums import DocumentType
from core.exceptions import CoreValidationError
from core.credit_applications.enums import ApplicationStatus

class PortugalPolicy(CountryPolicy):
    """
    Country-specific business rules for Portugal (PT).
    """

    MAX_INCOME_MULTIPLIER = Decimal("20")
    # Pre-compiled regex for better performance
    NIF_REGEX = re.compile(r"^[0-9]{9}$")

    def validate(self, application):
        self._validate_document_type(application.applicant.document.document_type)
        self._validate_document_format(application.applicant.document.value)

    def _validate_document_type(self, document_type):
        if document_type != DocumentType.NIF:
            raise CoreValidationError("Portugal requires NIF document")

    def _validate_document_format(self, nif: str) -> None:
        if not self.NIF_REGEX.match(nif):
            raise CoreValidationError("Policy Error: Invalid NIF format")

        # Optional: PT NIFs usually start with 1, 2, 3, 5, 6, 8, or 9
        if nif[0] not in "1235689":
             raise CoreValidationError("Invalid NIF: unrecognized starting digit")

        digits = [int(d) for d in nif]
        
        # Calculate checksum using weights 9 down to 2
        total = sum(d * (9 - i) for i, d in enumerate(digits[:8]))

        remainder = total % 11
        check_digit = 0 if remainder < 2 else 11 - remainder

        if digits[8] != check_digit:
            raise CoreValidationError("Policy Error: Invalid NIF control digit")            

    def evaluate(self, application):
        monthly_income = application.monthly_income.monthly_amount
        max_allowed = monthly_income * self.MAX_INCOME_MULTIPLIER
        #f"Policy Error: Requested amount exceeds the {self.MAX_INCOME_MULTIPLIER}x "
        # "income limit for Portugal"

        if application.requested_amount.amount > max_allowed:
            return ApplicationStatus.REJECTED

        return ApplicationStatus.VALIDATED