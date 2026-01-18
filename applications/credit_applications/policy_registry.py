from core.credit_applications.enums import Country
from core.policies.spain import SpainPolicy
from core.policies.portugal import PortugalPolicy
from core.exceptions import ValidationError


_POLICIES = {
    Country.SP: SpainPolicy(),
    Country.PT: PortugalPolicy(),
}


def get_policy(country: Country):
    """
    Returns the credit policy for a given country.

    Selection is an application concern.
    Policies themselves remain pure domain objects.
    """
    try:
        return _POLICIES[country]
    except KeyError:
        raise ValidationError(
            f"No credit policy registered for country {country}"
        )
