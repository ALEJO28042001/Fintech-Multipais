from core.policies.base import CreditPolicy
from core.credit_applications.enums import DocumentType
from core.exceptions import ValidationError

class ColombiaPolicy(CreditPolicy):

    def validate_application(self, application):
        doc_type = application.applicant.document.document_type

        if doc_type not in {DocumentType.CC}:
            raise ValidationError(
                "Invalid document type for Colombia"
            )
