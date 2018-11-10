from decimal import getcontext, ROUND_UP, Decimal
from typing import Optional, List

from constants import CURRENCY
from enums import UnitType
from utils import list_printout, as_currency

# We're an evil grocery store so we will round up the price $$$
getcontext().rounding = ROUND_UP


class Grocery:
    def __init__(self, name, price_per_unit, quantity=Decimal('1'), unit_type=UnitType.UNIT):
        self.name = name
        self.price_per_unit = price_per_unit
        self.quantity = quantity
        self.unit_type = unit_type

    def __repr__(self):
        return f'{self.quantity} {self.name} ({CURRENCY}{self.price_per_unit}/{self.unit_type.value}) ' \
               f'for a total price of {as_currency(self.price)}'

    def __add__(self, other):
        return self.price + other.price

    def __radd__(self, other):
        return self.price + other

    def __lt__(self, other):
        return self.price < other.price

    @property
    def price(self):
        return round(self.price_per_unit * self.quantity, 2)


class Basket:
    def __init__(self, groceries):
        self.groceries = groceries
        self.total_price = round(sum(groceries), 2)

    def __repr__(self):
        return list_printout(self.groceries)

    def __iter__(self):
        yield from self.groceries


class DiscountRule:
    def __init__(self, description: str, rule_callable):
        """
        `rule_callable` defines how the discount behaves.
        It takes in a list of groceries and outputs a reduction as a Decimal if it can find one to apply.
        """
        self.description = description
        self.rule_callable = rule_callable

    def __repr__(self):
        return self.description

    def __call__(self, groceries) -> Optional[Decimal]:
        return self.rule_callable(groceries)


class Discount:
    def __init__(self, rule: DiscountRule):
        self.rule = rule
        self.reduction = Decimal('0')

    def __repr__(self):
        return f"Reduction: {as_currency(self.reduction)} / {self.rule.description}"

    def __add__(self, other):
        return self.reduction + other.reduction

    def __radd__(self, other):
        return self.reduction + other

    def apply(self, basket):
        reduction = self.rule(basket)
        if reduction is not None:
            self.reduction = reduction
            return True
        return False


class Store:
    def __init__(self, discounts: Optional[List[Discount]]=None):
        if discounts is None:
            discounts = []
        self.discounts = discounts

    def checkout(self, basket: Basket, extra_discounts: List[Discount]=None):
        if extra_discounts is None:
            extra_discounts = []

        applicable_discounts = self.discounts + extra_discounts
        successful_discounts = self._apply_discounts(basket, applicable_discounts)
        total_reduction_discounts = sum(successful_discounts)

        # We add instead of subtract since reduction is a negative number
        total_price = basket.total_price + total_reduction_discounts

        return Receipt(
            total_price=total_price,
            basket=basket,
            discounts=successful_discounts,
            total_reduction_discounts=total_reduction_discounts
        )

    def _apply_discounts(self, basket, discounts):
        successful_discounts = []
        for discount in discounts:
            if discount.apply(basket):
                successful_discounts.append(discount)
        return successful_discounts


class Receipt:
    """
    The receipt for the customer.
    Acts as a proof of payment.
    On the receipt the customer can any information regarding his or her purchase.
    """
    def __init__(self,
                 total_price,
                 basket,
                 discounts=None,
                 total_reduction_discounts=Decimal('0')):
        if discounts is None:
            discounts = []
        self.total_price = total_price
        self.basket = basket
        self.discounts = discounts
        self.total_reduction_discounts = total_reduction_discounts

    def __repr__(self):
        """
        Proper way to handle this would be to use the textwrap library as this will get rid of the ugly indentation
        in the code. For now this works just fine.
        """
        return f"""\
You've purchased:
{self.basket}

Total price groceries: {as_currency(self.basket.total_price)}
{self.discount_printout()}
-----------------------------
- Your final total is: {as_currency(self.total_price)}
-----------------------------

Thank you and please come again!\
"""

    def discount_printout(self):
        if not self.discounts:
            return 'No discounts to apply'

        return f"""\

Your discounts:
{list_printout(self.discounts)}

Total discount: {as_currency(self.total_reduction_discounts)}
"""
