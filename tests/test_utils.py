from decimal import Decimal

import pytest

from utils import list_printout, as_currency


def test_receipt_item_printout():
    class TestObject:
        def __repr__(self):
            return 'TestObject'

    assert list_printout([TestObject(), TestObject(), TestObject()]) == f'TestObject\nTestObject\nTestObject'


@pytest.mark.parametrize('decimal, expected', (
    (Decimal('1'), '$1.00'),
    (Decimal('0'), '$0.00'),
    (Decimal('1.23'), '$1.23'),
    (Decimal('1.2'), '$1.20'),
    (Decimal('1.20'), '$1.20'),
    (Decimal('1.200001'), '$1.21'),
    (Decimal('1.209'), '$1.21'),
    (Decimal('1.20501'), '$1.21'),
    (Decimal('0.12'), '$0.12'),
))
def test_as_currency(decimal, expected):
    assert as_currency(decimal) == expected