"""
Tests for the expect any type
"""

import pytest

from jestspectation import Any, Anything

TYPE_TESTS = [
    (str, "string"),
    (int, 42),
    (float, 42.0),
    (list, [1, 2, 3, 4, 5]),
    (set, {1, 2, 3, 4, 5}),
    (dict, {"a": 1, "b": 2, "c": 3}),
    (type, int),
]


@pytest.mark.parametrize(
    ("type", "instance"),
    TYPE_TESTS,
)
def test_matches_self(type, instance):
    assert Any(type) == instance


def test_matches_subclass():
    class MyInt(int):
        pass

    assert Any(int) == MyInt(42)


def test_doesnt_match_wrong_type():
    assert Any(int) != "not an int"


def test_any_get_diff():
    assert Any(int).get_diff("my str", False) == [
        "Any(int) == 'my str'",
        "Type mismatch",
        "Expected any object of type int",
        "Received 'my str' (str)",
    ]


@pytest.mark.parametrize(
    ("type", "instance"),
    TYPE_TESTS,
)
def test_match_anything(type, instance):
    assert Anything() == instance
