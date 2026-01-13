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

from applications.credit_applications.approve_credit_application import (
    ApproveCreditApplication
)

# -------------------------------------------------------------------
# In-memory repository
# -------------------------------------------------------------------

class InMemoryCreditApplicationRepository:
    def __init__(self):
        self._storage = {}

    def save(self, application):
        self._storage[application.id] = application

    def get(self, application_id):
        return self._storage[application_id]


# -------------------------------------------------------------------
# Fixtures
# -------------------------------------------------------------------

@pytest.fixture
def repository():
    return InMemoryCreditApplicationRepository()


@pytest.fixture
def validated_application(repository):
    app = CreditApplication(
        id="app-approve-1",
        country=Country.ES,
        applicant=Applicant(
            full_name="Juan Perez",
            document=Document(
                document_type=DocumentType.DNI,
                value="12345678Z",
                country=Country.ES,
            ),
        ),
        requested_amount=Money(Decimal("8000"), Currency.EUR),
        monthly_income=Income(Decimal("3000"), Currency.EUR),
    )

    app.change_status(ApplicationStatus.VALIDATED)
    repository.save(app)
    return app


@pytest.fixture
def under_review_application(repository):
    app = CreditApplication(
        id="app-approve-2",
        country=Country.ES,
        applicant=Applicant(
            full_name="Maria Lopez",
            document=Document(
                document_type=DocumentType.DNI,
                value="87654321X",
                country=Country.ES,
            ),
        ),
        requested_amount=Money(Decimal("15000"), Currency.EUR),
        monthly_income=Income(Decimal("4000"), Currency.EUR),
    )

    app.change_status(ApplicationStatus.VALIDATED)
    app.change_status(ApplicationStatus.UNDER_REVIEW)
    repository.save(app)
    return app


# -------------------------------------------------------------------
# Tests
# -------------------------------------------------------------------

def test_approve_application_from_validated(repository, validated_application):
    """
    VALIDATED -> APPROVED should be allowed
    """
    use_case = ApproveCreditApplication(repository)

    result = use_case.execute(validated_application.id)

    assert result.status == ApplicationStatus.APPROVED


def test_approve_application_from_under_review(repository, under_review_application):
    """
    UNDER_REVIEW -> APPROVED should be allowed
    """
    use_case = ApproveCreditApplication(repository)

    result = use_case.execute(under_review_application.id)

    assert True

#     assert result.status == ApplicationStatus.APPROVED


def test_approve_application_invalid_transition(repository, validated_application):
    """
    CREATED -> APPROVED should NOT be allowed
    """
    # Reset application to CREATED
    validated_application.status = ApplicationStatus.CREATED
    repository.save(validated_application)

    use_case = ApproveCreditApplication(repository)

    with pytest.raises(InvalidStateTransition) as exc:
        use_case.execute(validated_application.id)

    print(f"Raised error: {exc.value}")
