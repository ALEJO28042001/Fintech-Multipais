from core.credit_applications import (
    CreditApplication,
    Applicant,
)
from core.credit_applications.enums import ApplicationStatus
from applications.credit_applications.policy_registry import get_policy

class CreateCreditApplication:
    def execute(self, application: CreditApplication) -> CreditApplication:
        policy = get_policy(application.country)

        policy.validate(application)

        outcome = policy.evaluate(application)

        application.change_status(outcome)

        return application


