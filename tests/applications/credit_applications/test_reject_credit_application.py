import pytest
from decimal import Decimal

from core.credit_applications.entities import CreditApplication, Applicant
from core.credit_applications.enums import (
    ApplicationStatus,
    Country,
    DocumentType,
    Currency,
)
from core.credit_applications.value_objects import Money, Income, Document
from core.exceptions import InvalidStateTransition

from applications.credit_applications import (
    RejectCreditApplication
)
from tests.fakes.repositories.in_memory_credit_application_repository import InMemoryCreditApplicationRepository

from core.exceptions import CoreError

# -------------------------------------------------------------------
# Fixtures
# -------------------------------------------------------------------

@pytest.fixture
def repository():
    return InMemoryCreditApplicationRepository()


@pytest.fixture
def credit_application(repository):
    app = CreditApplication(
        id="app-reject-1",
        country=Country.PT,
        applicant=Applicant(
            full_name="João Silva",
            document=Document(
                document_type=DocumentType.NIF,
                value="123456789",
                country=Country.PT,
            ),
        ),
        requested_amount=Money(Decimal("5000"), Currency.EUR),
        monthly_income=Income(Decimal("2000"), Currency.EUR),
    )

    repository.save(app)
    return app


# -------------------------------------------------------------------
# Tests
# -------------------------------------------------------------------

def test_reject_application_from_created(repository, credit_application):
    """
    CREATED -> REJECTED should be allowed
    """
    use_case = RejectCreditApplication(repository)

    result = use_case.execute(
        application_id=credit_application.id,
        reason="Policy rejection",
    )

    assert result.status == ApplicationStatus.REJECTED


def test_reject_application_invalid_transition(repository, credit_application):
    """
    Rejecting an already APPROVED application should fail
    """
    credit_application.change_status(ApplicationStatus.VALIDATED)
    credit_application.change_status(ApplicationStatus.APPROVED)
    repository.save(credit_application)

    use_case = RejectCreditApplication(repository)

    with pytest.raises(CoreError) as exc:
        use_case.execute(
            application_id=credit_application.id,
            reason="Too late",
        )

    print(f"Raised error: {exc.value}")
