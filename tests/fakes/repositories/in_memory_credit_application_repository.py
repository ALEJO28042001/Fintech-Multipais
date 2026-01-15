from core.credit_applications.repository import CreditApplicationRepository

class InMemoryCreditApplicationRepository(CreditApplicationRepository):

    def __init__(self):
        self._data = {}

    def get(self, application_id: str):
        return self._data.get(application_id)

    def save(self, application):
        self._data[application.id] = application

