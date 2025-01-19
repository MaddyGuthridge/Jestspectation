"""
Tests for logical combinators
"""

from jestspectation import Any, Not


def test_not_inverts():
    assert Not(Any(int)) == "not an int"
    assert Not(Any(int)) != 1


def test_not_literals():
    assert Not("nice") == 68


def test_diff():
    diff = Not(Any(str)).get_diff("my str", False)
    assert diff == [
        "Any(str) != 'my str'",
        "Unwanted match",
        "Expected object that doesn't match with Any(str)",
        "Received 'my str'",
    ]
