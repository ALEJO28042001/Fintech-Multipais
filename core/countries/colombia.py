from core.countries.base import CountryPolicy
from core.credit_applications.enums import DocumentType
from core.exceptions import CoreValidationError

class ColombiaPolicy(CountryPolicy):

    def validate_application(self, application):
        doc_type = application.applicant.document.document_type

        if doc_type not in {DocumentType.CC}:
            raise CoreValidationError(
                "Invalid document type for Colombia"
            )
