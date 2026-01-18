from core.policies.base import CreditPolicy
from core.credit_applications.enums import DocumentType
from core.exceptions import ValidationError
import re
from decimal import Decimal
from core.credit_applications.enums import ApplicationStatus

class SpainPolicy(CreditPolicy):

    """
    Country-specific business rules for Spain (SP).
    """

    REVIEW_THRESHOLD = Decimal("10000")

    def validate(self, application):
        self._validate_document_type(application.applicant.document.document_type)
        self._validate_document_format(application.applicant.document.value)

    def _validate_document_type(self, document_type):
        if document_type != DocumentType.DNI:
            raise ValidationError(
                "Policy Error: Spain requires DNI document"
            )

    def _validate_document_format(self, dni: str) -> None:
        if not re.match(r"^[0-9]{8}[A-Z]$", dni):
            raise ValidationError("Policy Error: Invalid DNI format")
        
    def evaluate(self, application):
        if application.requested_amount.amount > self.REVIEW_THRESHOLD:
            return ApplicationStatus.UNDER_REVIEW

        return ApplicationStatus.VALIDATED