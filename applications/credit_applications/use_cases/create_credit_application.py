from core.credit_applications import (
    CreditApplication,
    Applicant,
)
from core.credit_applications.repository import CreditApplicationRepository
from applications.credit_applications.policy_registry import get_policy
from core.exceptions import CoreError

class CreateCreditApplication:
    def __init__(self, repository: CreditApplicationRepository):
        self.repository = repository

    def execute(self, application: CreditApplication) -> CreditApplication:
        if self.repository.get(application.id):
            raise CoreError("Core Error: Can not create the Credit application, already exists")

        policy = get_policy(application.country)

        # Phase 1: creation-level validation
        policy.validate(application)
        self.repository.save(application)  # CREATED

        # Phase 2: business decision
        outcome = policy.evaluate(application)
        application.change_status(outcome)
        self.repository.save(application)  # FINAL STATE

        return application




