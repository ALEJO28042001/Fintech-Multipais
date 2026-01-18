from core.credit_applications import (
    CreditApplication,
    Applicant,
)
from core.credit_applications.repository import CreditApplicationRepository
from core.exceptions import CoreError

class CreateCreditApplication:
    def __init__(
        self,
        repository: CreditApplicationRepository,
        policy_provider,
    ):
        self.repository = repository
        self.policy_provider = policy_provider


    def execute(self, application: CreditApplication) -> CreditApplication:
        if self.repository.get(application.id):
            raise CoreError("Core Error: Can not create the Credit application, already exists")

        policy = self.policy_provider(application.country)

        # Phase 1: creation-level validation
        policy.validate(application)
        self.repository.save(application)  # CREATED

        # Phase 2: business decision
        outcome = policy.evaluate(application)
        application.change_status(outcome)
        self.repository.save(application)  # FINAL STATE

        return application




