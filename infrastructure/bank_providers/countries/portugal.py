from infrastructure.bank_providers import BankProvider
from typing import Dict, Any
from core.credit_applications import BankSnapshot



class PortugalBankProvider(BankProvider):
    def fetch_data(self, document_number: str) -> Dict[str, Any]:
        # Requirement 3.3: Variations in data delivery
        return {
            "monthly_debt_load": 400.00,
            "credit_score": 680,
            "nif_status": "active"
        }

    def map_to_snapshot(self, payload: Dict[str, Any]) -> BankSnapshot:
        return BankSnapshot(
            provider="PortugalBank",
            payload=payload
        )