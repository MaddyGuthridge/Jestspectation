"""
Tests for logical combinators
"""
from jestspectation import And, Not, Any, StringMatchingRegex


def test_and_not_all_match():
    assert And(Any(int), Any(str)) != 1


def test_and_all_match():
    assert And(Any(str), Not(StringMatchingRegex('hello*'))) == "Goodbye world"


def test_diff():
    diff = And(Any(int), Any(str)).get_diff(1)
    assert diff == [
        "And(Any(int), Any(str)) == 1",
        "Not all matches fulfilled",
        "1 failed to match with",
        "-- Any(str) == 1",
        "   Type mismatch",
        "   Expected any object of type str",
        "   Received 1 (int)",
    ]
