"""Hypothesis fuzz tests and fixed regressions for all three functions.

The validation policy is documented in README.md. Invalid inputs return None.
Run these SAME tests against the original snapshot to reproduce the failures.
"""

from decimal import Decimal
import math

import pytest
from hypothesis import given, settings, strategies as st

from movie_tickets import average_rating, parse_seat, total_price

FUZZ = settings(
    max_examples=300, derandomize=True, deadline=None,
    report_multiple_bugs=False, database=None,
)
TEXT_OR_NONE = st.text() | st.none()
NON_STRINGS = st.one_of(
    st.none(), st.booleans(), st.integers(), st.floats(), st.binary(),
    st.lists(st.integers(), max_size=10),
    st.dictionaries(st.text(max_size=10), st.integers(), max_size=5),
)


@FUZZ
@given(TEXT_OR_NONE)
def test_parse_seat_no_crash(s):
    result = parse_seat(s)
    if result is not None:
        row, number = result
        assert row in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        assert type(number) is int and number > 0


@FUZZ
@given(TEXT_OR_NONE)
def test_total_price_no_crash(s):
    result = total_price(s)
    assert result is None or (
        type(result) is float and math.isfinite(result) and result >= 0
    )


@FUZZ
@given(TEXT_OR_NONE)
def test_average_rating_no_crash(s):
    result = average_rating(s)
    assert result is None or (
        type(result) is float and math.isfinite(result) and 1 <= result <= 5
    )


@FUZZ
@given(NON_STRINGS)
def test_all_functions_reject_non_strings(s):
    for function in (parse_seat, total_price, average_rating):
        assert function(s) is None


@FUZZ
@given(st.sampled_from('ABCDEFGHIJKLMNOPQRSTUVWXYZ'), st.integers(1, 10**12))
def test_valid_seat_round_trip(row, number):
    assert parse_seat(f'{row}{number}') == (row, number)
    assert parse_seat(f' \t{row.lower()}00{number} \n') == (row, number)


@FUZZ
@given(st.lists(st.integers(0, 10**9), min_size=1, max_size=30))
def test_valid_prices_match_independent_decimal_oracle(prices):
    csv = ','.join(str(p) for p in prices)
    expected = float(Decimal(sum(prices)) * Decimal('1.18'))
    assert total_price(csv) == expected
    assert total_price(', '.join(str(p) for p in reversed(prices))) == expected


@FUZZ
@given(st.integers(0, 10**9), st.integers(0, 10**9))
def test_adding_a_nonnegative_price_cannot_reduce_total(first, extra):
    assert total_price(f'{first},{extra}') >= total_price(str(first))


@FUZZ
@given(st.lists(st.integers(1, 5), min_size=1, max_size=100))
def test_valid_rating_average_and_order_invariance(ratings):
    text = ' '.join(str(r) for r in ratings)
    expected = round(sum(ratings) / len(ratings), 1)
    assert average_rating(text) == expected
    assert average_rating('\t'.join(str(r) for r in reversed(ratings))) == expected
    assert min(ratings) <= average_rating(text) <= max(ratings)


@FUZZ
@given(st.integers(1, 5), st.integers(1, 100))
def test_repeated_rating_has_the_same_average(rating, count):
    assert average_rating(' '.join([str(rating)] * count)) == float(rating)


@pytest.mark.parametrize('seat', [
    None, '', ' ', 'H', '12', 'H0', 'H-1', 'HH12', 'H1.5', 'H 12',
    '\u00e912', 'H\u0661', 'H1\x00', '\ud800', 'A' + '1' * 4096,
])
def test_invalid_seat_regressions(seat):
    assert parse_seat(seat) is None


@pytest.mark.parametrize('csv', [
    None, '', ' ', ',', '150,,250', '150,', ',150', '-1', '150,-250',
    'one,two', '1.5', 'NaN', 'Infinity', '\u0661', '1\x00', '1' * 400,
    '1' * 4097,
])
def test_invalid_price_regressions(csv):
    assert total_price(csv) is None


@pytest.mark.parametrize('ratings', [
    None, '', ' \t\n', '0', '6', '-1', '4 0 5', '4 6 5', '1.5',
    'NaN', 'Infinity', 'four five', '4,5', '\u0661', '1\x00', '1' * 4097,
])
def test_invalid_rating_regressions(ratings):
    assert average_rating(ratings) is None


@pytest.mark.parametrize('function,valid_at_limit', [
    (parse_seat, 'H' + '0' * 4094 + '1'),
    (total_price, '0' * 4095 + '1'),
    (average_rating, ' ' * 4095 + '1'),
])
def test_input_length_boundary(function, valid_at_limit):
    assert len(valid_at_limit) == 4096
    assert function(valid_at_limit) is not None
    assert function(valid_at_limit + ' ') is None


def test_zero_price_and_invalid_token_atomicity():
    assert total_price('0') == 0.0
    assert total_price('150,not-a-price,250') is None


def test_known_valid_examples():
    assert parse_seat('H12') == ('H', 12)
    assert total_price('150,250,400') == 944.0
    assert average_rating('4 5 3') == 4.0
