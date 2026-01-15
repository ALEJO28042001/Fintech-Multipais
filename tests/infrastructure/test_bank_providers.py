import pytest

from core.credit_applications.enums import Country
from infrastructure.bank_providers import get_bank_provider
from infrastructure.bank_providers import (
    BankProvider,
    SpainBankProvider,
    PortugalBankProvider,
)


# -------------------------------------------------------
# Happy path
# -------------------------------------------------------

def test_factory_returns_spain_provider():
    provider = get_bank_provider(Country.ES)

    assert isinstance(provider, SpainBankProvider)
    assert isinstance(provider, BankProvider)


def test_factory_returns_portugal_provider():
    provider = get_bank_provider(Country.PT)

    assert isinstance(provider, PortugalBankProvider)
    assert isinstance(provider, BankProvider)


# -------------------------------------------------------
# Failure cases (expected)
# -------------------------------------------------------

def test_factory_raises_for_unsupported_country():
    with pytest.raises(ValueError) as exc:
        get_bank_provider(Country.BR)

    print(f"Raised error: {exc.value}")


def test_factory_raises_for_invalid_type():
    with pytest.raises(TypeError) as exc:
        get_bank_provider("ES")  # wrong type

    print(f"Raised error: {exc.value}")


def test_factory_raises_for_none():
    with pytest.raises(TypeError) as exc:
        get_bank_provider(None)

    print(f"Raised error: {exc.value}")
