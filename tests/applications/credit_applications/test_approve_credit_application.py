import pytest

from applications.credit_applications import AttachBankSnapshot,ApproveCreditApplication

from core.credit_applications.enums import ApplicationStatus
from core.exceptions import CoreError
from tests.fakes.repositories.in_memory_credit_application_repository import InMemoryCreditApplicationRepository
from infrastructure.bank_providers import get_bank_provider
from applications.credit_applications import CreateCreditApplication
from core.credit_applications.enums import Country
from core.credit_applications.entities import CreditApplication, Applicant
from core.credit_applications.value_objects import Money, Income, Document
from core.credit_applications.enums import Currency, DocumentType
from decimal import Decimal


def created_spain_application(repository):
    use_case = CreateCreditApplication(repository)

    app = CreditApplication(
        id="app-SP-1",
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

    return use_case.execute(app)

def test_attach_bank_snapshot_spain():
    repository = InMemoryCreditApplicationRepository()
    application = created_spain_application(repository)
    # --- Attach bank snapshot ---
    attach_uc = AttachBankSnapshot(repository)
    attach_uc.execute(application.id)

    # --- Approve application ---
    approve_uc = ApproveCreditApplication(repository)
    result = approve_uc.execute(application.id)

    # --- Final assertions only ---
    assert result.status == ApplicationStatus.APPROVED
    assert result.bank_snapshot is not None
    assert result.bank_snapshot.provider == "SpainBank"



