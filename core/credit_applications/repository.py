from abc import ABC, abstractmethod
from core.credit_applications.entities import CreditApplication

class CreditApplicationRepository(ABC):

    @abstractmethod
    def get(self, application_id: str) -> CreditApplication | None:
        pass

    @abstractmethod
    def save(self, application: CreditApplication) -> None:
        pass
