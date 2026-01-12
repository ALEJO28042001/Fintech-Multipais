import pytest
from decimal import Decimal

from core.countries.spain import SpainPolicy
from core.credit_applications.entities import CreditApplication, Applicant
from core.credit_applications.value_objects import Money, Income, Document
from core.credit_applications.enums import (
    Currency,
    Country,
    DocumentType,
)
from core.exceptions import CoreValidationError

def test_spain_accepts_valid_dni():
    policy = SpainPolicy()

    app = CreditApplication(
        id="app-1",
        country=Country.ES,
        applicant=Applicant(
            full_name="Juan Perez",
            document=Document(
                document_type=DocumentType.DNI,
                value="12345678Z",
                country=Country.ES,
            ),
        ),
        requested_amount=Money(Decimal("9000"), Currency.EUR),
        monthly_income=Income(Decimal("2000"), Currency.EUR),
    )

    policy.validate(app)  # should not raise

def test_spain_rejects_non_dni():
    policy = SpainPolicy()

    app = CreditApplication(
        id="app-1",
        country=Country.ES,
        applicant=Applicant(
            full_name="Juan Perez",
            document=Document(
                document_type=DocumentType.DNI,
                value="123456788",
                country=Country.ES,
            ),
        ),
        requested_amount=Money(Decimal("9000"), Currency.EUR),
        monthly_income=Income(Decimal("2000"), Currency.EUR),
    )

    with pytest.raises(CoreValidationError) as exc_info:
        policy.validate(app)

    print("EXPECTED ERROR:", exc_info.value)
