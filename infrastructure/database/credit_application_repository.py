from core.credit_applications.repository import CreditApplicationRepository

class DjangoCreditApplicationRepository(CreditApplicationRepository):

    def get(self, application_id: str):
        # ORM logic
        ...

    def save(self, application):
        # ORM logic
        ...
