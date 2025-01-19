"""
Tests / Pytest test

Wow this is so meta
"""
from jestspectation import Equals
from jestspectation.pytest import pytest_assertrepr_compare


def test_get_diff():
    assert pytest_assertrepr_compare(
        None,  # type: ignore
        "==",
        Equals(2),
        1,
    ) == [
        "2 == 1",
        "Value mismatch",
        "Expected 2",
        "Received 1",
    ]


def test_get_diff_reverse():
    assert pytest_assertrepr_compare(
        None,  # type: ignore
        "==",
        1,
        Equals(2),
    ) == [
        "1 == 2",
        "Value mismatch",
        "Expected 2",
        "Received 1",
    ]


def test_incompatible():
    """
    Test when we are given an operation that is unsupported by Jestspectation
    """
    assert pytest_assertrepr_compare(
        None,  # type: ignore
        "<=",
        1,
        Equals(2),
    ) is None
