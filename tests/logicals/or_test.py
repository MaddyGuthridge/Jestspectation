"""
Tests for logical combinators
"""
from jestspectation import Not, Or, Any, StringMatchingRegex


def test_or_not_all_match():
    assert Or(Any(int), Any(str)) == 1


def test_or_none_match():
    assert Or(Any(int), Any(str)) != 1.0


def test_or_all_match():
    assert Or(Any(str), Not(StringMatchingRegex('hello*'))) == "Goodbye world"
