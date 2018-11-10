from decimal import Decimal

from discount_rules import buy_two_apples_get_one_free
from factories import DiscountFactory, BasketFactory, GroceryFactory


def test_discount_apply_correctly_discounts():
    grocery = GroceryFactory(name='Apples', price_per_unit=Decimal('2'), quantity=Decimal('3'))
    basket = BasketFactory(groceries=[grocery])
    discount = DiscountFactory(rule=buy_two_apples_get_one_free)
    discount.apply(basket)
    assert discount.reduction == Decimal('-2')


def test_discount_apply_correctly_discounts_multiple_groceries():
    grocery1 = GroceryFactory(name='Apples', price_per_unit=Decimal('2'), quantity=Decimal('3'))
    grocery2 = GroceryFactory(name='Milk', price_per_unit=Decimal('2'), quantity=Decimal('3'))
    grocery3 = GroceryFactory(name='Red Wine', price_per_unit=Decimal('5'), quantity=Decimal('1'))
    basket = BasketFactory(groceries=[grocery1, grocery2, grocery3])
    discount = DiscountFactory(rule=buy_two_apples_get_one_free)
    discount.apply(basket)
    assert discount.reduction == Decimal('-2')
