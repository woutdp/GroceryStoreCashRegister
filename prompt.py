import random
import sys
import time
from decimal import Decimal

from discount_rules import buy_two_apples_get_one_free, five_off_when_you_spend_hundred_or_more
from enums import UnitType
from factories import GroceryFactory
from objects import Grocery, Basket, Store, Discount


def _random_price():
    return round(Decimal(random.randrange(10, 1000) / 100), 2)


def _random_quantity(natural_number=True):
    if natural_number:
        return Decimal(random.randint(1, 40))
    return round(Decimal(random.randrange(10, 1000) / 100), 2)


def _delay_print(message, delay=0.03):
    for character in message:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(delay)
    print('\n')


def generate_groceries():
    all_groceries = [Grocery('Apples', price_per_unit=Decimal('1.20'), quantity=Decimal('3'))]
    all_groceries += [GroceryFactory(price_per_unit=_random_price(),
                                     quantity=_random_quantity(False),
                                     unit_type=UnitType.KILOGRAM) for _ in range(7)]
    all_groceries += [GroceryFactory(price_per_unit=_random_price(),
                                     quantity=_random_quantity(),
                                     unit_type=UnitType.UNIT) for _ in range(7)]
    return sorted(all_groceries)


def generate_store():
    return Store(discounts=[Discount(rule=buy_two_apples_get_one_free)])


def print_intro():
    print('Hello and welcome to my store!')
    print("My name is Wout, I'll guide you around.")
    print('I have a crazy assortment of goods, and when I say crazy I mean it.')
    print("Check it out! I've ordered them from cheap to expensive.")
    print('Also try the apples, they are delicious. If you buy 3, you get 1 for free!')


def print_options():
    print('--')
    for index, grocery in enumerate(all_groceries):
        print(f'{index}) {grocery}')
    print('--')


def get_choice():
    print('Please make a selection of items you want to buy.')
    print('Example: for item 1 6 and 10, type: `1 6 10`')

    choice = []
    while(not choice):
        try:
            choice = [int(i) for i in input('Your choice: ').rstrip().split(' ') if len(all_groceries) > int(i) >= 0]
            choice = sorted(list(set(choice)))  # Sort and get rid of any duplicates
            if not choice:
                print("I don't know these numbers.")
        except ValueError:  # Very naughty
            print('Nice try, use numbers only.')

    print('')
    print('')
    return choice


def generate_basket(choice):
    return Basket([all_groceries[i] for i in choice])


def print_basket():
    print("You've chosen the following items:")
    print('--')
    print(basket)
    print('--')
    print('Nice choice ;)')
    print('')
    print('Now, maybe you have some coupon with you?')


def get_extra_discounts():
    valid_coupon_code = 'WineDirect'

    time.sleep(2.50)
    _delay_print(f"------ A gollum wispers in your ear: "
                 f"'Hint, enter the coupon code `{valid_coupon_code}` for $5 off if your order is larger than $100.'")

    coupon_code = input('Coupon code: ')

    extra_discounts = []
    if coupon_code.lower() == valid_coupon_code.lower():
        extra_discounts += [Discount(rule=five_off_when_you_spend_hundred_or_more)]
        print('That looks like a valid coupon code! I wonder where you got it from..')
    else:
        print("Hmm I don't know this coupon code, better luck next time!")

    return extra_discounts


def generate_receipt(extra_discounts):
    return store.checkout(basket, extra_discounts=extra_discounts)


def print_receipt():
    time.sleep(1)
    _delay_print('Let me just count them up, give me a second...')
    time.sleep(1)
    _delay_print('Done! Here is your receipt.')
    time.sleep(0.5)

    print('')
    print('')
    print('RECEIPT')
    print('--------------------------------------------------')
    print(receipt)
    print('--------------------------------------------------')
    print('')
    print('')
    time.sleep(2)


def print_door():
    _delay_print('Thank you!')
    time.sleep(1)
    _delay_print("Here's the door.")
    print('''\
     ______________
    |\ ___________ /|
    | |  /|,| |   | |
    | | |,x,| |   | |
    | | |,x,' |   | |
    | | |,x   ,   | |
    | | |/    |%==| |
    | |    /] ,   | |
    | |   [/ ()   | |
    | |       |   | |
    | |       |   | |
    | |       |   | |
    | |      ,'   | |
    | |   ,'      | |
    |_|,'_________|_|
    ''')
    print('')
    input('Press any key to exit.')


all_groceries = generate_groceries()
store = generate_store()
print_intro()
print_options()
basket = generate_basket(get_choice())
print_basket()
receipt = generate_receipt(get_extra_discounts())
print_receipt()
print_door()
