from decimal import Decimal

from enums import UnitType
from objects import DiscountRule


def buy_two_apples_get_one_free_rule(basket):
    for grocery in basket:
        if grocery.name == 'Apples' and grocery.unit_type == UnitType.UNIT:
            return Decimal(-(grocery.quantity // 3 * grocery.price_per_unit))

buy_two_apples_get_one_free = DiscountRule(
    description='Buy two Apples and get one free.',
    rule_callable=buy_two_apples_get_one_free_rule
)


def five_off_when_you_spend_hundred_or_more_rule(basket):
    if basket.total_price >= 100:
        return Decimal('-5')

five_off_when_you_spend_hundred_or_more = DiscountRule(
    description='5 off when you spend 100 or more',
    rule_callable=five_off_when_you_spend_hundred_or_more_rule
)
