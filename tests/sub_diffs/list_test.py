"""
Tests for list sub-diffs
"""
from jestspectation.__py_diffs import diff_list


def test_diff_list_equal():
    assert diff_list([1, 2, 3], [1, 2, 3], False) is None


def test_diff_list_type():
    assert diff_list([1, 2, 3], {1, 2, 3}, False) == [
        "[1, 2, 3] == {1, 2, 3}",
        "Type mismatch",
        "Expected list",
        "Received set",
    ]


def test_diff_list_not_equal():
    assert diff_list([1], [2], False) == [
        "[1] == [2]",
        '!! [0] 1 == 2',
        '   Value mismatch',
        '   Expected 1',
        '   Received 2',
    ]


def test_diff_list_missing():
    assert diff_list([1], [], False) == [
        "[1] == []",
        '-- [0] 1',
    ]


def test_diff_list_additional():
    assert diff_list([], [1], False) == [
        "[] == [1]",
        '++ [0] 1',
    ]


def test_diff_list_combination():
    assert diff_list([1, 2, 3], [1, 3, 3, 4], False) == [
        "[1, 2, 3] == [1, 3, 3, 4]",
        '!! [1] 2 == 3',
        '   Value mismatch',
        '   Expected 2',
        '   Received 3',
        '++ [3] 4',
    ]
