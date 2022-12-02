"""
Tests for string matchers
"""
from jestspectation import StringContaining


def test_bad_type():
    assert StringContaining('hello') != 1


def test_match():
    assert StringContaining('hello') == 'hello world'


def test_no_match():
    assert StringContaining('hello') != 'goodbye world'


def test_diff_no_match():
    assert StringContaining('hello').get_diff('goodbye world', False) == [
        "StringContaining('hello') == 'goodbye world'",
        "String failed to match",
        "Expected StringContaining('hello')",
        "Received 'goodbye world'",
    ]


def test_diff_bad_type():
    assert StringContaining('hello').get_diff(1, False) == [
        "StringContaining('hello') == 1",
        "Type mismatch",
        "Expected object of type str (StringContaining('hello'))",
        "Received object of type int (1)",
    ]
