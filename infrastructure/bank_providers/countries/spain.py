from infrastructure.bank_providers import BankProvider
from typing import Dict, Any
from core.credit_applications import BankSnapshot


class SpainBankProvider(BankProvider):
    def fetch_data(self, document_number: str) -> Dict[str, Any]:
        # Spain might provide different fields, like a risk index
        return {
            "dni_verification": "verified",
            "risk_index": 0.12,
            "annual_income_estimate": 35000
        }

    def map_to_snapshot(self, payload: Dict[str, Any]) -> BankSnapshot:
        return BankSnapshot(
            provider="SpainBank",
            payload=payload
        )