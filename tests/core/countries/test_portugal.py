import pytest
from decimal import Decimal

from core.countries.portugal import PortugalPolicy
from core.credit_applications.entities import CreditApplication, Applicant
from core.credit_applications.value_objects import Money, Income, Document
from core.credit_applications.enums import (
    Country,
    Currency,
    DocumentType,
)
from core.exceptions import CoreValidationError

def test_portugal_accepts_valid_application():
    policy = PortugalPolicy()

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
        requested_amount=Money(Decimal("15000"), Currency.EUR),
        monthly_income=Income(Decimal("1000"), Currency.EUR),
    )

    # Should not raise
    policy.validate(app)

def test_portugal_rejects_non_nif_document():
    policy = PortugalPolicy()

    app = CreditApplication(
        id="app-pt-2",
        country=Country.PT,
        applicant=Applicant(
            full_name="João Silva",
            document=Document(
                document_type=DocumentType.CC,
                value="AA123456",
                country=Country.PT,
            ),
        ),
        requested_amount=Money(Decimal("5000"), Currency.EUR),
        monthly_income=Income(Decimal("2000"), Currency.EUR),
    )

    with pytest.raises(CoreValidationError) as exc_info:
        policy.validate(app)

    print("EXPECTED ERROR:", exc_info.value)

def test_portugal_rejects_unverified_document():
    policy = PortugalPolicy()

    app = CreditApplication(
        id="app-pt-3",
        country=Country.PT,
        applicant=Applicant(
            full_name="João Silva",
            document=Document(
                document_type=DocumentType.NIF,
                value="123456AA",
                country=Country.PT,
            ),
        ),
        requested_amount=Money(Decimal("5000"), Currency.EUR),
        monthly_income=Income(Decimal("2000"), Currency.EUR),
    )

    with pytest.raises(CoreValidationError) as exc_info:
        policy.validate(app)

    print("EXPECTED ERROR:", exc_info.value)