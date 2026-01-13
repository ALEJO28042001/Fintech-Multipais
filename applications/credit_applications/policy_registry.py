from core.countries import (
    SpainPolicy,
    PortugalPolicy,
)
from core.credit_applications.enums import Country

POLICIES = {
    Country.ES: SpainPolicy(),
    Country.PT: PortugalPolicy(),
}

def get_policy(country: Country):
    try:
        return POLICIES[country]
    except KeyError:
        raise ValueError(f"No policy registered for country {country}")
