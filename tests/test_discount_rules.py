from decimal import Decimal

from discount_rules import buy_two_apples_get_one_free, five_off_when_you_spend_hundred_or_more
from enums import UnitType
from factories import DiscountFactory, BasketFactory, GroceryFactory


class TestDiscountRuleBuyTwoApplesGetOneFree:
    def setup_method(self):
        self.discount = DiscountFactory(rule=buy_two_apples_get_one_free)

    def test_basic_case(self):
        basket = BasketFactory(groceries=[
            GroceryFactory(name='Oranges', price_per_unit=Decimal('2'), quantity=Decimal('3')),
            GroceryFactory(name='Cakes', price_per_unit=Decimal('10'), quantity=Decimal('2')),
            GroceryFactory(name='Apples', price_per_unit=Decimal('2.22'), quantity=Decimal('3'))
        ])
        self.discount.apply(basket)
        assert self.discount.reduction == Decimal('-2.22')

    def test_different_unit_type(self):
        basket = BasketFactory(groceries=[
            GroceryFactory(name='Oranges', price_per_unit=Decimal('2'), quantity=Decimal('3')),
            GroceryFactory(name='Cakes', price_per_unit=Decimal('10'), quantity=Decimal('2')),
            GroceryFactory(name='Apples', price_per_unit=Decimal('2.22'), quantity=Decimal('3'),
                           unit_type=UnitType.KILOGRAM)
        ])
        self.discount.apply(basket)
        assert self.discount.reduction == Decimal('0')

    def test_not_enough_apples(self):
        basket = BasketFactory(groceries=[
            GroceryFactory(name='Oranges', price_per_unit=Decimal('2'), quantity=Decimal('3')),
            GroceryFactory(name='Cakes', price_per_unit=Decimal('10'), quantity=Decimal('2')),
            GroceryFactory(name='Apples', price_per_unit=Decimal('2.22'), quantity=Decimal('2'))
        ])
        self.discount.apply(basket)
        assert self.discount.reduction == Decimal('0')

    def test_6_apples(self):
        basket = BasketFactory(groceries=[
            GroceryFactory(name='Oranges', price_per_unit=Decimal('2'), quantity=Decimal('3')),
            GroceryFactory(name='Cakes', price_per_unit=Decimal('10'), quantity=Decimal('2')),
            GroceryFactory(name='Apples', price_per_unit=Decimal('2.22'), quantity=Decimal('6'))
        ])
        self.discount.apply(basket)
        assert self.discount.reduction == Decimal('-4.44')

    def test_5_apples(self):
        basket = BasketFactory(groceries=[
            GroceryFactory(name='Oranges', price_per_unit=Decimal('2'), quantity=Decimal('3')),
            GroceryFactory(name='Cakes', price_per_unit=Decimal('10'), quantity=Decimal('2')),
            GroceryFactory(name='Apples', price_per_unit=Decimal('2.22'), quantity=Decimal('5'))
        ])
        self.discount.apply(basket)
        assert self.discount.reduction == Decimal('-2.22')

    def test_different_unit_type_and_correct_unit_type(self):
        basket = BasketFactory(groceries=[
            GroceryFactory(name='Oranges', price_per_unit=Decimal('2'), quantity=Decimal('3')),
            GroceryFactory(name='Cakes', price_per_unit=Decimal('10'), quantity=Decimal('2')),
            GroceryFactory(name='Apples', price_per_unit=Decimal('2.22'), quantity=Decimal('3'),
                           unit_type=UnitType.KILOGRAM),
            GroceryFactory(name='Apples', price_per_unit=Decimal('2.22'), quantity=Decimal('5'))
        ])
        self.discount.apply(basket)
        assert self.discount.reduction == Decimal('-2.22')


class TestFiveOffWhenYouSpendHundredOrMore:
    def setup_method(self):
        self.discount = DiscountFactory(rule=five_off_when_you_spend_hundred_or_more)

    def test_above_hundred(self):
        basket = BasketFactory(groceries=[
            GroceryFactory(name='Oranges', price_per_unit=Decimal('2'), quantity=Decimal('3')),
            GroceryFactory(name='Cakes', price_per_unit=Decimal('10'), quantity=Decimal('10')),
            GroceryFactory(name='Apples', price_per_unit=Decimal('2.22'), quantity=Decimal('5'))
        ])
        assert basket.total_price >= Decimal('100')
        self.discount.apply(basket)
        assert self.discount.reduction == Decimal('-5')

    def test_below_hundred(self):
        basket = BasketFactory(groceries=[
            GroceryFactory(name='Oranges', price_per_unit=Decimal('2'), quantity=Decimal('3')),
            GroceryFactory(name='Cakes', price_per_unit=Decimal('5'), quantity=Decimal('3')),
            GroceryFactory(name='Apples', price_per_unit=Decimal('2.22'), quantity=Decimal('5'))
        ])
        assert basket.total_price <= Decimal('100')
        self.discount.apply(basket)
        assert self.discount.reduction == Decimal('0')
