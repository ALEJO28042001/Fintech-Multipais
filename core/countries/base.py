from abc import ABC, abstractmethod
from core.credit_applications.entities import CreditApplication

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
