from decimal import Decimal
import pytest

from core.credit_applications.value_objects import Money, Income
from core.credit_applications.enums import Currency
from core.exceptions import ValidationError

def test_money_must_be_positive():
    with pytest.raises(ValidationError) as exc_info:
        Money(amount=Decimal("0"), currency=Currency.EUR)
    print("EXPECTED ERROR:", exc_info.value)

def test_income_must_be_positive():
        
    with pytest.raises(ValidationError) as exc_info:
        Income(monthly_amount=Decimal("-1"), currency=Currency.EUR)
    print("EXPECTED ERROR:", exc_info.value)