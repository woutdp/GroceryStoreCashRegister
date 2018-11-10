from decimal import Decimal
from typing import List

from constants import CURRENCY


def list_printout(list_of_objects: List) -> str:
    """
    Takes in a list of objects and outputs a string where each item in the list is separated by a new line.
    """
    return '\n'.join([str(i) for i in list_of_objects])


def as_currency(decimal: Decimal) -> str:
    return f'{CURRENCY}{round(decimal, 2)}'