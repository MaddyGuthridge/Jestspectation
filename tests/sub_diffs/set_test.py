"""
Tests for set sub-diffs
"""
from jestspectation.__py_diffs import diff_set


def test_diff_set_equal():
    assert diff_set({1, 2, 3}, {1, 2, 3}) is None


def test_diff_set_type():
    assert diff_set({1, 2, 3}, [1, 2, 3]) == [
        "{1, 2, 3} == [1, 2, 3]",
        "Type mismatch",
        "Expected set",
        "Received list",
    ]


def test_diff_set_missing():
    assert diff_set({1}, set()) == [
        "{1} == set()",
        '-- 1',
    ]


def test_diff_set_additional():
    assert diff_set(set(), {1}) == [
        "set() == {1}",
        '++ 1',
    ]


def test_diff_set_combination():
    assert diff_set({1, 2, 3}, {1, 3, 4}) == [
        "{1, 2, 3} == {1, 3, 4}",
        '-- 2',
        '++ 4',
    ]
