from core.exceptions import CoreError
from core.credit_applications.repository import CreditApplicationRepository
from core.credit_applications.enums import ApplicationStatus

class AttachBankSnapshot:
    def __init__(self, repository, bank_provider_selector):
        self.repository = repository
        self.bank_provider_selector = bank_provider_selector


    def execute(self, application_id: str):
        application = self.repository.get(application_id)

        # Optional but recommended state guard
        if application.status not in {
            ApplicationStatus.VALIDATED,
            ApplicationStatus.UNDER_REVIEW,
        }:
            raise CoreError(
                f"Cannot fetch bank data in state {application.status}"
            )

        provider = self.bank_provider_selector(application.country)

        if not provider:
            raise CoreError(
                f"No bank provider for country {application.country}"
            )

        bank_result = provider.fetch_data(application.applicant.document)
        snapshot = provider.map_to_snapshot(bank_result)
        application.attach_bank_snapshot(snapshot)
        self.repository.save(application)
        return application
