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
