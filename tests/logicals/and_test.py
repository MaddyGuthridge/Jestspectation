"""
Tests for logical combinators
"""
from jestspectation import And, Not, Any, StringMatchingRegex


def test_and_not_all_match():
    assert And(Any(int), Any(str)) != 1


def test_and_all_match():
    assert And(Any(str), Not(StringMatchingRegex('hello*'))) == "Goodbye world"
