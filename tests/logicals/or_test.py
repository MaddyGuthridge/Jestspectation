"""
Tests for logical combinators
"""
from jestspectation import Any, Not, Or, StringMatchingRegex


def test_or_not_all_match():
    assert Or(Any(int), Any(str)) == 1


def test_or_none_match():
    assert Or(Any(int), Any(str)) != 1.0


def test_or_all_match():
    assert Or(Any(str), Not(StringMatchingRegex('hello*'))) == "Goodbye world"


def test_diff():
    diff = Or(Any(int), Any(str)).get_diff(1.0, False)
    assert diff == [
        "Or(Any(int), Any(str)) == 1.0",
        "No matches fulfilled",
        "1.0 must match with at least one of",
        "-- Any(int) == 1.0",
        "   Type mismatch",
        "   Expected any object of type int",
        "   Received 1.0 (float)",
        "-- Any(str) == 1.0",
        "   Type mismatch",
        "   Expected any object of type str",
        "   Received 1.0 (float)",
    ]
