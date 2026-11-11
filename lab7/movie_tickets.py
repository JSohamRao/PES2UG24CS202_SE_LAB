"""Movie-ticket input processing hardened against malformed external data.

Valid inputs retain the original return types. Invalid input returns None;
the CLI displays an error and continues with the remaining functions.
See README.md for the explicit validation policy adopted for this lab.
"""

from fractions import Fraction
import math
import re

MAX_INPUT_LENGTH = 4096


def _validated_text(value):
    """Reject non-strings and oversized input before doing any conversion."""
    if not isinstance(value, str) or len(value) > MAX_INPUT_LENGTH:
        return None
    return value.strip()


def _ascii_integer(token):
    """Parse unsigned ASCII decimal digits without coercing other types."""
    if not token or not token.isascii() or not token.isdecimal():
        return None
    try:
        return int(token)
    except ValueError:
        # Respect a host-configured Python integer conversion limit too.
        return None


def parse_seat(seat):
    """Return (uppercase row A-Z, positive number), or None for invalid data."""
    text = _validated_text(seat)
    if not text or re.fullmatch(r'[A-Za-z][0-9]+', text) is None:
        return None
    number = _ascii_integer(text[1:])
    if number is None or number == 0:
        return None
    return text[0].upper(), number


def total_price(prices_csv):
    """Add 18% GST to nonnegative integer prices; reject an invalid CSV whole."""
    text = _validated_text(prices_csv)
    if not text:
        return None
    prices = [_ascii_integer(token.strip()) for token in text.split(',')]
    if any(price is None for price in prices):
        return None
    try:
        # Integer cents avoid binary-float multiplication errors before the
        # final conversion to the starter's float return type.
        total = float(Fraction(sum(prices) * 118, 100))
    except OverflowError:
        return None
    return total if math.isfinite(total) else None


def average_rating(ratings):
    """Average whitespace-separated integer ratings in 1-5, or return None."""
    text = _validated_text(ratings)
    if not text:
        return None
    values = [_ascii_integer(token) for token in text.split()]
    if any(value is None or not 1 <= value <= 5 for value in values):
        return None
    return round(sum(values) / len(values), 1)


def main():
    """Run the three prompts without letting invalid input terminate the app."""
    prompts = [
        ('parse_seat', 'Enter a seat number (e.g. H12): ', parse_seat,
         'Row and Seat:', 'Invalid seat; use a row A-Z and a positive number.'),
        ('total_price', 'Enter ticket prices as CSV (e.g. 150,250,400): ',
         total_price, 'Total with GST:',
         'Invalid prices; use nonnegative integers separated by commas.'),
        ('average_rating', 'Enter ratings separated by spaces (e.g. 4 5 3): ',
         average_rating, 'Average Rating:',
         'Invalid ratings; use integers from 1 to 5 separated by spaces.'),
    ]
    for name, prompt, function, label, error in prompts:
        print(f'==== Running {name} ====')
        try:
            user_input = input(prompt)
        except (EOFError, KeyboardInterrupt):
            print('\nInput cancelled.')
            return
        result = function(user_input)
        if result is None:
            print(error)
        else:
            print(label, result)
        print()


if __name__ == '__main__':
    main()
