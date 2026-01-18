from core.credit_applications.enums import Country
from core.exceptions import ValidationError

from infrastructure.bank_providers.base import BankProvider
from infrastructure.bank_providers.countries.spain import SpainBankProvider
from infrastructure.bank_providers.countries.portugal import PortugalBankProvider


_PROVIDERS: dict[Country, type[BankProvider]] = {
    Country.SP: SpainBankProvider,
    Country.PT: PortugalBankProvider,
}


def get_bank_provider(country: Country) -> BankProvider:
    if not isinstance(country, Country):
        raise TypeError(
            f"country must be a Country enum, got {type(country).__name__}"
        )

    try:
        return _PROVIDERS[country]()
    except KeyError:
        raise ValidationError(
            f"No bank provider configured for country '{country.name}'"
        )
