from hypothesis import given, strategies as st
from movie_tickets import parse_seat, total_price, average_rating

@given(st.text() | st.none())
def test_parse_seat_no_crash(s):

@given(st.text() | st.none())
def test_total_price_no_crash(s):

@given(st.text() | st.none())
def test_average_rating_no_crash(s):
