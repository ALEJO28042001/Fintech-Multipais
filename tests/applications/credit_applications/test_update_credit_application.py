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

from applications.credit_applications.update_application_state import (
    UpdateCreditApplicationState
)

# -------------------------------------------------------------------
# In-memory test repository
# -------------------------------------------------------------------

class InMemoryCreditApplicationRepository:
    def __init__(self):
        self._storage = {}

    def save(self, application: CreditApplication):
        self._storage[application.id] = application

    def get(self, application_id: str) -> CreditApplication:
        return self._storage[application_id]


# -------------------------------------------------------------------
# Fixtures
# -------------------------------------------------------------------

@pytest.fixture
def repository():
    return InMemoryCreditApplicationRepository()


@pytest.fixture
def credit_application(repository):
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
        requested_amount=Money(Decimal("5000"), Currency.EUR),
        monthly_income=Income(Decimal("2000"), Currency.EUR),
    )

    repository.save(app)
    return app


# -------------------------------------------------------------------
# Tests
# -------------------------------------------------------------------

def test_update_application_state_valid_transition(repository, credit_application):
    """
    CREATED -> VALIDATED should succeed
    """
    use_case = UpdateCreditApplicationState(repository)

    result = use_case.execute(
        application_id=credit_application.id,
        new_status=ApplicationStatus.VALIDATED,
    )

    assert result.status == ApplicationStatus.VALIDATED


def test_update_application_state_invalid_transition(repository, credit_application):
    """
    CREATED -> APPROVED should fail
    """
    use_case = UpdateCreditApplicationState(repository)

    with pytest.raises(InvalidStateTransition) as exc:
        use_case.execute(
            application_id=credit_application.id,
            new_status=ApplicationStatus.APPROVED,
        )

    print(f"Raised error: {exc.value}")


def test_update_application_state_persists_change(repository, credit_application):
    """
    Ensure repository is updated
    """
    use_case = UpdateCreditApplicationState(repository)

    use_case.execute(
        application_id=credit_application.id,
        new_status=ApplicationStatus.VALIDATED,
    )

    stored = repository.get(credit_application.id)
    assert stored.status == ApplicationStatus.VALIDATED
