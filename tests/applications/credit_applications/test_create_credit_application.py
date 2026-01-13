import pytest
from decimal import Decimal
from applications.credit_applications.use_cases import CreateCreditApplication
from core.credit_applications.entities import CreditApplication, Applicant
from core.credit_applications.value_objects import Money, Income, Document
from core.credit_applications.enums import (
    Country,
    Currency,
    DocumentType,
    ApplicationStatus,
)
from core.exceptions import CoreValidationError

def test_create_spain_application_validated():
    use_case = CreateCreditApplication()

    app = CreditApplication(
        id="app-es-1",
        country=Country.ES,
        applicant=Applicant(
            full_name="Juan Perez",
            document=Document(
                document_type=DocumentType.DNI,
                value="12345678Z",
                country=Country.ES,
            ),
        ),
        requested_amount=Money(Decimal("5000"), Currency.EUR),
        monthly_income=Income(Decimal("2000"), Currency.EUR),
    )

    result = use_case.execute(app)

    assert result.status == ApplicationStatus.VALIDATED

def test_create_spain_application_under_review():
    use_case = CreateCreditApplication()

    app = CreditApplication(
        id="app-es-2",
        country=Country.ES,
        applicant=Applicant(
            full_name="Juan Perez",
            document=Document(
                document_type=DocumentType.DNI,
                value="12345678Z",
                country=Country.ES,
            ),
        ),
        requested_amount=Money(Decimal("15000"), Currency.EUR),
        monthly_income=Income(Decimal("3000"), Currency.EUR),
    )

    result = use_case.execute(app)

    assert result.status == ApplicationStatus.UNDER_REVIEW

def test_create_portugal_application_rejected_by_policy():
    use_case = CreateCreditApplication()

    app = CreditApplication(
        id="app-pt-1",
        country=Country.PT,
        applicant=Applicant(
            full_name="João Silva",
            document=Document(
                document_type=DocumentType.NIF,
                value="123456789",
                country=Country.PT,
            ),
        ),
        requested_amount=Money(Decimal("30000"), Currency.EUR),
        monthly_income=Income(Decimal("1000"), Currency.EUR),
    )

    result = use_case.execute(app)

    assert result.status == ApplicationStatus.REJECTED

def test_create_portugal_application_validated():
    use_case = CreateCreditApplication()

    app = CreditApplication(
        id="app-pt-2",
        country=Country.PT,
        applicant=Applicant(
            full_name="João Silva",
            document=Document(
                document_type=DocumentType.NIF,
                value="123456789",
                country=Country.PT,
            ),
        ),
        requested_amount=Money(Decimal("15000"), Currency.EUR),
        monthly_income=Income(Decimal("1000"), Currency.EUR),
    )

    result = use_case.execute(app)

    assert result.status == ApplicationStatus.VALIDATED
