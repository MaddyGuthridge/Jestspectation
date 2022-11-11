"""
Tests for logical combinators
"""
import pytest
from jestspectation import And, Not, Or, Xor, Any, StringMatchingRegex


@pytest.mark.parametrize(
    'matcher_type',
    [
        And,
        Or,
        Xor
    ]
)
def test_too_few_enough_matchers(matcher_type):
    with pytest.raises(TypeError):
        # Requires at least two matchers
        matcher_type(Any(int))


def test_not_inverts():
    assert Not(Any(int)) == "not an int"
    assert Not(Any(int)) != 1


def test_not_literals():
    assert 68 == Not("nice")


def test_and_not_all_match():
    assert And(Any(int), Any(str)) != 1


def test_and_all_match():
    assert And(Any(str), Not(StringMatchingRegex('hello*'))) == "Goodbye world"


def test_or_not_all_match():
    assert Or(Any(int), Any(str)) == 1


def test_or_none_match():
    assert Or(Any(int), Any(str)) != 1.0


def test_or_all_match():
    assert Or(Any(str), Not(StringMatchingRegex('hello*'))) == "Goodbye world"


def test_xor_not_all_match():
    assert Xor(Any(int), Any(str)) == 1


def test_xor_none_match():
    assert Xor(Any(int), Any(str)) != 1.0


def test_xor_all_match():
    assert Xor(Any(str), Not(StringMatchingRegex('hello*'))) != "Goodbye world"
