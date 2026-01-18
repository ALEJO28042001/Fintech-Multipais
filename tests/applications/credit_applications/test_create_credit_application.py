import pytest
from decimal import Decimal
from core.exceptions import CoreError

from applications.credit_applications import CreateCreditApplication
from core.credit_applications.entities import CreditApplication, Applicant
from core.credit_applications.value_objects import Money, Income, Document
from core.credit_applications.enums import (
    Country,
    Currency,
    DocumentType,
    ApplicationStatus,
)
from tests.fakes.repositories.in_memory_credit_application_repository import InMemoryCreditApplicationRepository

def test_create_credit_application_success():
    # Arrange
    repository = InMemoryCreditApplicationRepository()
    use_case = CreateCreditApplication(repository=repository)

    application = CreditApplication(
        id="app-1",
        country=Country.SP,
        applicant=Applicant(
            full_name="Juan Perez",
            document=Document(
                document_type=DocumentType.DNI,
                value="12345678Z",
                country=Country.SP,
            ),
        ),
        requested_amount=Money(Decimal("5000"), Currency.EUR),
        monthly_income=Income(Decimal("2000"), Currency.EUR),
    )

    # Act
    result = use_case.execute(application)

    # Assert
    assert result.id == "app-1"
    assert result.status == ApplicationStatus.VALIDATED
    assert repository.get("app-1") is not None

def test_create_credit_application_twice_fails():
    repository = InMemoryCreditApplicationRepository()
    use_case = CreateCreditApplication(repository=repository)

    application = CreditApplication(
        id="app-1",
        country=Country.SP,
        applicant=Applicant(
            full_name="Juan Perez",
            document=Document(
                document_type=DocumentType.DNI,
                value="12345678Z",
                country=Country.SP,
            ),
        ),
        requested_amount=Money(Decimal("5000"), Currency.EUR),
        monthly_income=Income(Decimal("2000"), Currency.EUR),
    )

    # First creation → OK
    use_case.execute(application)

    # Second creation → FAIL
    with pytest.raises(CoreError) as exc:
        use_case.execute(application)

    print(f"Raised error: {exc.value}")

def test_create_credit_application_invalid_document_fails():
    repository = InMemoryCreditApplicationRepository()
    use_case = CreateCreditApplication(repository=repository)

    application = CreditApplication(
        id="app-2",
        country=Country.SP,
        applicant=Applicant(
            full_name="Juan Perez",
            document=Document(
                document_type=DocumentType.NIF,  # ❌ Portugal document
                value="123456789",
                country=Country.PT,
            ),
        ),
        requested_amount=Money(Decimal("5000"), Currency.EUR),
        monthly_income=Income(Decimal("2000"), Currency.EUR),
    )

    with pytest.raises(CoreError) as exc:
        use_case.execute(application)

    print(f"Raised error: {exc.value}")
