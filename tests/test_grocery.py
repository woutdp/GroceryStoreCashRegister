from decimal import Decimal

import pytest

from enums import UnitType
from factories import GroceryFactory


@pytest.mark.parametrize('name, price_per_unit, quantity, unit_type, expected_printout', (
    ('Apples', Decimal('1'), Decimal('2'), UnitType.UNIT,
     '2 Apples ($1/Unit) for a total price of $2.00'),
    ('Oranges', Decimal('1.5'), Decimal('4'), UnitType.KILOGRAM,
     '4 Oranges ($1.5/kg) for a total price of $6.00'),
    ('Pears', Decimal('0.22'), Decimal('3'), UnitType.UNIT,
     '3 Pears ($0.22/Unit) for a total price of $0.66'),
    ('Jalopeño Peppers', Decimal('0.222'), Decimal('3'), UnitType.KILOGRAM,
     '3 Jalopeño Peppers ($0.222/kg) for a total price of $0.67'),
))
def test_grocery_print_output(name, price_per_unit, quantity, unit_type, expected_printout):
    grocery = GroceryFactory(
        name=name,
        price_per_unit=price_per_unit,
        quantity=quantity,
        unit_type=unit_type,
    )
    assert str(grocery) == expected_printout


def test_groceries_add_up_together():
    grocery1 = GroceryFactory(price_per_unit=Decimal('1.333'), quantity=Decimal('2'))  # 2.67
    grocery2 = GroceryFactory(price_per_unit=Decimal('0.4'), quantity=Decimal('1.5'))  # 0.6
    assert grocery1 + grocery2 == Decimal('3.27')


def test_groceries_add_up_together_through_sum():
    grocery1 = GroceryFactory(price_per_unit=Decimal('1.333'), quantity=Decimal('2'))  # 2.67
    grocery2 = GroceryFactory(price_per_unit=Decimal('0.4'), quantity=Decimal('1.5'))  # 0.6
    assert sum([grocery1 + grocery2]) == Decimal('3.27')


@pytest.mark.parametrize('price_per_unit, quantity, expected_price', (
    (Decimal('1'), Decimal('2'), Decimal('2')),
    (Decimal('1.5'), Decimal('4'), Decimal('6')),
    (Decimal('0.22'), Decimal('3'), Decimal('0.66')),
    (Decimal('0.222'), Decimal('3'), Decimal('0.67')),
    (Decimal('10000'), Decimal('1000'), Decimal('10000000')),
    (Decimal('0'), Decimal('3'), Decimal('0')),
))
def test_grocery_price_calculation(price_per_unit, quantity, expected_price):
    assert GroceryFactory(price_per_unit=price_per_unit, quantity=quantity).price == expected_price
