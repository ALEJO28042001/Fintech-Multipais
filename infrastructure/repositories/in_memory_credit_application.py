from core.credit_applications.repository import (
    CreditApplicationRepository,
)
from core.exceptions import NotFoundError


class InMemoryCreditApplicationRepository(CreditApplicationRepository):

    def __init__(self):
        self._data = {}

    def get(self, application_id: str):
        return self._data.get(application_id)

    def list(self, country=None, status=None):
        results = self._data.values()

        if country:
            results = [a for a in results if a.country == country]
        if status:
            results = [a for a in results if a.status.value == status]

        return list(results)

    def save(self, application):
        self._data[application.id] = application
