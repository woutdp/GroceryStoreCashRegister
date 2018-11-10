from decimal import Decimal

from factories import GroceryFactory
from objects import Basket


def test_basket_correctly_adds_up_total_price():
    grocery1 = GroceryFactory(price_per_unit=Decimal('1'), quantity=Decimal('1'))  # 1
    grocery2 = GroceryFactory(price_per_unit=Decimal('2'), quantity=Decimal('2'))  # 4
    grocery3 = GroceryFactory(price_per_unit=Decimal('3'), quantity=Decimal('3'))  # 9
    assert Basket([grocery1, grocery2, grocery3]).total_price == Decimal('14')
