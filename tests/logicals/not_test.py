"""
Tests for logical combinators
"""
from jestspectation import Not, Any


def test_not_inverts():
    assert Not(Any(int)) == "not an int"
    assert Not(Any(int)) != 1


def test_not_literals():
    assert 68 == Not("nice")
