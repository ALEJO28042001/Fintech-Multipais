from decimal import Decimal
from datetime import datetime
import pytest

from core.credit_applications.entities import CreditApplication, Applicant
from core.credit_applications.value_objects import Money, Income, Document
from core.credit_applications.enums import (
    Currency,
    Country,
    DocumentType,
    ApplicationStatus,
)
from core.exceptions import InvalidStateTransition

def test_valid_status_transition():
    app = CreditApplication(
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
        requested_amount=Money(Decimal("1000"), Currency.EUR),
        monthly_income=Income(Decimal("2000"), Currency.EUR),
    )

    app.change_status(ApplicationStatus.VALIDATED)

    assert app.status == ApplicationStatus.VALIDATED

def test_invalid_status_transition():
    app = CreditApplication(
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
        requested_amount=Money(Decimal("1000"), Currency.EUR),
        monthly_income=Income(Decimal("2000"), Currency.EUR),
    )

    with pytest.raises(InvalidStateTransition):
        app.change_status(ApplicationStatus.APPROVED)
