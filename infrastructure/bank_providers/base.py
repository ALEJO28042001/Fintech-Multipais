from abc import ABC, abstractmethod
from typing import Dict, Any
from core.credit_applications import BankSnapshot


class BankProvider(ABC):
    @abstractmethod
    def fetch_data(self, document_number: str) -> Dict[str, Any]:
        """Client Role: Call the external API and return raw JSON."""
        pass

    @abstractmethod
    def map_to_snapshot(self, payload: Dict[str, Any]) -> BankSnapshot:
        """Adapter Role: Transform raw JSON into the immutable domain snapshot."""
        pass