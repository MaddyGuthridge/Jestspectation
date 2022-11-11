"""
Tests for logical combinators
"""
from jestspectation import Not, Xor, Any, StringMatchingRegex


def test_xor_not_all_match():
    assert Xor(Any(int), Any(str)) == 1


def test_xor_none_match():
    assert Xor(Any(int), Any(str)) != 1.0


def test_xor_all_match():
    assert Xor(Any(str), Not(StringMatchingRegex('hello*'))) != "Goodbye world"


def test_diff_none():
    diff = Xor(Any(int), Any(str)).get_diff(1.0)
    assert diff == [
        "Xor(Any(int), Any(str)) == 1.0",
        "No matches fulfilled",
        "1.0 must match with exactly one of",
        "-- Any(int) == 1.0",
        "   Type mismatch",
        "   Expected any object of type int",
        "   Received 1.0 (float)",
        "-- Any(str) == 1.0",
        "   Type mismatch",
        "   Expected any object of type str",
        "   Received 1.0 (float)",
    ]


def test_diff_all():
    diff = Xor(Any(str), Not(StringMatchingRegex('hello*')))\
        .get_diff("Goodbye world")
    assert diff == [
        "Xor(Any(str), Not(StringMatchingRegex('hello*'))) == 'Goodbye world'",
        "Too many matches fulfilled",
        "'Goodbye world' matched with",
        "++ Any(str) == 'Goodbye world'",
        "++ Not(StringMatchingRegex('hello*')) == 'Goodbye world'",
        "But should only have matched with one of them",
    ]
