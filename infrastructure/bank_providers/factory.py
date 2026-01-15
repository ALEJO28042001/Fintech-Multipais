from core.credit_applications.enums import Country
from infrastructure.bank_providers.countries.spain import SpainBankProvider
from infrastructure.bank_providers.countries.portugal import PortugalBankProvider



_PROVIDERS = {
    Country.ES: SpainBankProvider,
    Country.PT: PortugalBankProvider,
}


def get_bank_provider(country: Country):
    if not isinstance(country, Country):
        raise TypeError(
            f"country must be a Country enum, got {type(country).__name__}"
        )

    try:
        return _PROVIDERS[country]()
    except KeyError:
        raise ValueError(f"No bank provider configured for country {country}")
