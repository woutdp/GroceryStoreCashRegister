import random
from decimal import Decimal

from factory import Factory, LazyAttribute, List, SubFactory
from faker import Faker
from faker.providers import BaseProvider

from constants import POSSIBLE_GROCERY_ITEMS
from objects import Grocery, Receipt, Discount, DiscountRule, Basket

fake = Faker()

class GroceryProvider(BaseProvider):
    def grocery(self):
        return random.choice(POSSIBLE_GROCERY_ITEMS)

fake.add_provider(GroceryProvider)


class GroceryFactory(Factory):
    class Meta:
        model = Grocery

    name = LazyAttribute(lambda x: fake.grocery())
    price_per_unit = Decimal('3')


class BasketFactory(Factory):
    class Meta:
        model = Basket

    groceries = List([SubFactory(GroceryFactory, price_per_unit=5) for _ in range(3)])


class DiscountRuleFactory(Factory):
    class Meta:
        model = DiscountRule

    description = 'This discount simply never applies and always returns 0'
    rule_callable = lambda x: Decimal('0')


class DiscountFactory(Factory):
    class Meta:
        model = Discount

    rule = SubFactory(DiscountRuleFactory)


class ReceiptFactory(Factory):
    class Meta:
        model = Receipt

    total_price = Decimal('10')
    basket = SubFactory(BasketFactory)
    discounts = List([SubFactory(DiscountFactory) for _ in range(2)])
    total_reduction_discounts = Decimal('5')
