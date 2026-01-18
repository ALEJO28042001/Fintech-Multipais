# ------------------------------------------------------------------------------
# Infrastructure
# ------------------------------------------------------------------------------
from infrastructure.repositories.in_memory_credit_application import (
    InMemoryCreditApplicationRepository,
)
from infrastructure.repositories.postgres_credit_application import (
    PostgresCreditApplicationRepository,
)
from infrastructure.bank_providers.registry import get_bank_provider
# ------------------------------------------------------------------------------
# Application use cases
# ------------------------------------------------------------------------------

from applications.credit_applications.use_cases.create_credit_application import (
    CreateCreditApplication,
)
from applications.credit_applications.use_cases.get_credit_application import (
    GetCreditApplication,
)
from applications.credit_applications.use_cases.list_credit_applications import (
    ListCreditApplications,
)
from applications.credit_applications.use_cases.attach_bank_snapshot import (
    AttachBankSnapshot,
)
from applications.credit_applications.use_cases.approve_credit_application import (
    ApproveCreditApplication,
)
from applications.credit_applications.use_cases.reject_credit_application import (
    RejectCreditApplication,
)

from applications.credit_applications.policy_registry import get_policy

# NOTE:
# This is the ONLY place where infrastructure is selected.
# Swap this to Postgres later without touching use cases or routers.

# _repository = InMemoryCreditApplicationRepository()
_repository = PostgresCreditApplicationRepository()


def get_credit_application_repository():
    return _repository


# ------------------------------------------------------------------------------
# Use case providers
# ------------------------------------------------------------------------------

def get_create_credit_application():
    return CreateCreditApplication(
        repository=get_credit_application_repository(),
        policy_provider=get_policy,
    )


def get_credit_application():
    return GetCreditApplication(
        repository=get_credit_application_repository(),
    )


def get_list_credit_applications():
    return ListCreditApplications(
        repository=get_credit_application_repository(),
    )


def get_attach_bank_snapshot():
    return AttachBankSnapshot(
        repository=get_credit_application_repository(),
        bank_provider_selector=get_bank_provider,
    )


def get_approve_credit_application():
    return ApproveCreditApplication(
        repository=get_credit_application_repository(),
    )


def get_reject_credit_application():
    return RejectCreditApplication(
        repository=get_credit_application_repository(),
    )
