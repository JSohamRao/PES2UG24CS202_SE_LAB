"""Stage 2: decision outcomes, boundary values and interacting discounts.

Expected prices are fixed examples, calculated independently of the code.
Coverage.py measures control-flow branches, not individual boolean operands.
"""

import pytest

from movie_tickets import group_discount, snack_combo, ticket_price


@pytest.mark.parametrize(
    "seat,age,hour,weekend,expected",
    [
        ("regular", 25, 0, False, 100),
        ("regular", 25, 11, False, 100),
        ("regular", 25, 12, False, 150),
        ("regular", 25, 17, False, 150),
        ("regular", 25, 18, False, 180),
        ("regular", 25, 23, False, 180),
        ("regular", 25, 12, True, 190),
        ("regular", 25, 11, True, 140),
        ("regular", 25, 18, True, 220),
        ("premium", 25, 12, False, 250),
        ("premium", 25, 11, False, 200),
        ("premium", 25, 18, True, 320),
        ("recliner", 25, 12, False, 400),
        ("recliner", 25, 11, True, 390),
        ("recliner", 25, 18, False, 430),
        ("regular", 2, 12, False, 0),
        ("recliner", 2, 18, True, 0),
        ("regular", 3, 12, False, 75),
        ("regular", 12, 12, False, 75),
        ("regular", 13, 12, False, 150),
        ("regular", 59, 12, False, 150),
        ("regular", 60, 12, False, 75),
        ("regular", 61, 12, False, 75),
        ("premium", 12, 11, True, 120),
        ("recliner", 60, 18, True, 235),
    ],
)
def test_ticket_decisions_and_boundaries(seat, age, hour, weekend, expected):
    assert ticket_price(seat, age, hour, weekend) == expected


@pytest.mark.parametrize("seat", ["vip", "", "Regular"])
def test_unknown_seat(seat):
    with pytest.raises(ValueError, match="^unknown seat$"):
        ticket_price(seat, 25, 12, False)


@pytest.mark.parametrize("hour", [-1, 24])
def test_both_invalid_time_limits(hour):
    with pytest.raises(ValueError, match="^invalid show time$"):
        ticket_price("regular", 25, hour, False)


@pytest.mark.parametrize("tickets", [-1, 0])
@pytest.mark.parametrize("student", [False, True])
def test_invalid_group_size(tickets, student):
    with pytest.raises(ValueError, match="^no tickets$"):
        group_discount(tickets, student)


@pytest.mark.parametrize(
    "tickets,student,expected",
    [
        (1, False, 0), (1, True, 0),
        (4, False, 0), (4, True, 0),
        (5, False, 10), (5, True, 15),
        (9, False, 10), (9, True, 15),
        (10, False, 15), (10, True, 20),
        (11, False, 15), (11, True, 20),
    ],
)
def test_group_thresholds_and_student_condition(tickets, student, expected):
    assert group_discount(tickets, student) == expected


@pytest.mark.parametrize(
    "size,coupon,expected",
    [
        ("small", False, 120), ("small", True, 70),
        ("medium", False, 180), ("medium", True, 130),
        ("large", False, 250), ("large", True, 200),
        ("unknown", False, 250), ("unknown", True, 200),
    ],
)
def test_snack_sizes_coupon_and_default(size, coupon, expected):
    # The supplied application intentionally uses its default price for
    # every size other than small/medium; no new validation is introduced.
    assert snack_combo(size, coupon) == expected
