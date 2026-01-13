from abc import ABC, abstractmethod
from core.credit_applications.entities import CreditApplication
from core.credit_applications.enums import ApplicationStatus

class CountryPolicy(ABC):
    """
    Base contract for country-specific business rules.
    """

    @abstractmethod
    def validate(self, application: CreditApplication) -> None:
        """
        Raises CoreValidationError if the application is invalid.
        """
        pass

    @abstractmethod
    def evaluate(self, application) -> bool:
        """
        Decide de outcome if the application is valid.
        """
        pass