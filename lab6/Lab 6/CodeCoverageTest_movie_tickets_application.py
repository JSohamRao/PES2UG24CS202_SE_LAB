"""Stage 1: execute every statement and assert the resulting behaviour."""

import pytest

from movie_tickets import group_discount, snack_combo, ticket_price


@pytest.mark.parametrize(
    "seat,age,hour,weekend,expected",
    [
        ("regular", 25, 15, False, 150),
        ("premium", 25, 10, True, 240),
        ("recliner", 25, 20, False, 430),
        ("regular", 2, 15, False, 0),
        ("regular", 60, 15, False, 75),
    ],
)
def test_ticket_statements(seat, age, hour, weekend, expected):
    assert ticket_price(seat, age, hour, weekend) == expected


@pytest.mark.parametrize(
    "seat,hour,message",
    [("vip", 15, "unknown seat"), ("regular", -1, "invalid show time")],
)
def test_ticket_error_statements(seat, hour, message):
    with pytest.raises(ValueError, match=f"^{message}$"):
        ticket_price(seat, 25, hour, False)


@pytest.mark.parametrize(
    "tickets,student,expected", [(2, False, 0), (5, False, 10), (10, True, 20)]
)
def test_group_statements(tickets, student, expected):
    assert group_discount(tickets, student) == expected


def test_group_error_statement():
    with pytest.raises(ValueError, match="^no tickets$"):
        group_discount(0, False)


@pytest.mark.parametrize(
    "size,coupon,expected",
    [("small", False, 120), ("medium", False, 180), ("large", True, 200)],
)
def test_snack_statements(size, coupon, expected):
    assert snack_combo(size, coupon) == expected
