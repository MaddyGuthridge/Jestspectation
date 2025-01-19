"""
Tests for set sub-diffs
"""

from jestspectation.__py_diffs import diff_dict


def test_diff_dict_equal():
    assert (
        diff_dict({"a": 1, "b": 2, "c": 3}, {"a": 1, "b": 2, "c": 3}, False)
        is None
    )


def test_diff_dict_type():
    assert diff_dict({"a": 1, "b": 2, "c": 3}, [1, 2, 3], False) == [
        "{'a': 1, 'b': 2, 'c': 3} == [1, 2, 3]",
        "Type mismatch",
        "Expected dict",
        "Received list",
    ]


def test_diff_dict_missing():
    assert diff_dict({"a": 1}, {}, False) == [
        "{'a': 1} == {}",
        "-- 'a': 1",
    ]


def test_diff_dict_additional():
    assert diff_dict({}, {"a": 1}, False) == [
        "{} == {'a': 1}",
        "++ 'a': 1",
    ]


def test_diff_dict_not_equal():
    assert diff_dict({"a": 1}, {"a": 2}, False) == [
        "{'a': 1} == {'a': 2}",
        "!! 'a': 1 == 'a': 2",
        "   1 == 2",
        "   Value mismatch",
        "   Expected 1",
        "   Received 2",
    ]


def test_diff_dict_combination():
    assert diff_dict(
        {"a": 1, "b": 2, "c": 3, "d": 4},
        {"a": 1, "b": 3, "d": 4, "e": 5},
        False,
    ) == [
        "{'a': 1, 'b': 2, 'c': 3, 'd': 4} == {'a': 1, 'b': 3, 'd': 4, 'e': 5}",
        "-- 'c': 3",
        "++ 'e': 5",
        "!! 'b': 2 == 'b': 3",
        "   2 == 3",
        "   Value mismatch",
        "   Expected 2",
        "   Received 3",
    ]
