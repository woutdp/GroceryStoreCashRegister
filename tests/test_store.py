from decimal import Decimal

from discount_rules import buy_two_apples_get_one_free, five_off_when_you_spend_hundred_or_more
from enums import UnitType
from factories import GroceryFactory
from objects import Store, Basket, Discount


def test_store_with_discounts():
    # Create a store where you can buy things. Set default discounts.
    store = Store(discounts=[Discount(rule=buy_two_apples_get_one_free)])

    # Fill your basket with groceries
    basket = Basket(groceries=[
        GroceryFactory(name='Oranges', price_per_unit=Decimal('4.4492'), quantity=Decimal('0.67'),
                       unit_type=UnitType.KILOGRAM),
        GroceryFactory(name='Cakes', price_per_unit=Decimal('100'), quantity=Decimal('2')),  # Very expensive cakes!
        GroceryFactory(name='Apples', price_per_unit=Decimal('2.22'), quantity=Decimal('5'))
    ])

    # Go to the checkout with your basket and your discount that you unlocked through a coupon.
    receipt = store.checkout(
        basket,
        extra_discounts=[
            Discount(rule=five_off_when_you_spend_hundred_or_more)
        ]
    )

    assert receipt.basket.total_price == Decimal('214.09')
    assert receipt.total_reduction_discounts == Decimal('-7.22')
    assert receipt.total_price == Decimal('206.87')
    assert str(receipt) == """\
You've purchased:
0.67 Oranges ($4.4492/kg) for a total price of $2.99
2 Cakes ($100/Unit) for a total price of $200.00
5 Apples ($2.22/Unit) for a total price of $11.10

Total price groceries: $214.09

Your discounts:
Reduction: $-2.22 / Buy two Apples and get one free.
Reduction: $-5.00 / 5 off when you spend 100 or more

Total discount: $-7.22

-----------------------------
- Your final total is: $206.87
-----------------------------

Thank you and please come again!\
"""


def test_store_without_discounts():
    # Create a store where you can buy things. Set default discounts.
    store = Store()

    # Fill your basket with groceries.
    basket = Basket(groceries=[
        GroceryFactory(name='Oranges', price_per_unit=Decimal('3'), quantity=Decimal('0.5'),
                       unit_type=UnitType.KILOGRAM),
        GroceryFactory(name='Cakes', price_per_unit=Decimal('10'), quantity=Decimal('1')),
        GroceryFactory(name='Apples', price_per_unit=Decimal('1'), quantity=Decimal('5'))
    ])

    # Go to the checkout with your basket.
    receipt = store.checkout(basket)

    assert receipt.basket.total_price == Decimal('16.5')
    assert receipt.total_reduction_discounts == Decimal('0')
    assert receipt.total_price == Decimal('16.5')
    assert str(receipt) == """\
You've purchased:
0.5 Oranges ($3/kg) for a total price of $1.50
1 Cakes ($10/Unit) for a total price of $10.00
5 Apples ($1/Unit) for a total price of $5.00

Total price groceries: $16.50
No discounts to apply
-----------------------------
- Your final total is: $16.50
-----------------------------

Thank you and please come again!\
"""
