# GroceryStoreCashRegister

A Grocery Store Cash Register with support for discounts.

## Quickstart
First clone the repository and `cd` into it.

### Docker
I've provided a quick way to get it up and running if you use docker. Simply run the following commands.

Get an interactive prompt for a super cool shopping experience that shows of the functionality.
```commandline
docker-compose run --rm groceries python ./prompt.py
```

Run tests.
```commandline
docker-compose run --rm groceries python -m pytest -vv
```

### Virtualenv
If you prefer [virtualenv](https://virtualenv.pypa.io/en/latest/installation/) you can follow this process.

Install the dependencies. 
````commandline
pip install -r requirements.txt
````

Get an interactive prompt for a super cool shopping experience that shows of the functionality.
```commandline
python ./prompt.py
```

Run tests.
```commandline
pytest
```

## Objects
This program has a couple of objects to make your life easier. 
If you want to create your own shopping list, you have to know what they do.

You can also take a look at the tests to see how objects interact with each other.

### Grocery
A single thing you can buy. Has a price, an amount, and can be in Kilograms or single units.

### Basket
A collection of Grocery objects.

### Discount and DiscountRule
`./discount_rules.py` defines some predefined rules, but you can add extra ones to your liking.
A `Discount` contains a `DiscountRule`. When you go through the checkout process, `Discount` objects will have their
`reduction` attribute set to how much they will reduce your bill.

### Store
This is where you pay.
You provide the store with a set of default discounts that always act on every basket.
When you're ready to pay do:
```
store.checkout(basket, extra_discounts)
```

Basket is your `basket` with groceries and `extra_discount` is simply a list of discounts that you might have achieved through a coupon or some other means.

### Receipt
Acts as a proof of payment for the customer.
The `store.checkout` method returns a receipt.

You can `print` a receipt to get the information in the terminal.
