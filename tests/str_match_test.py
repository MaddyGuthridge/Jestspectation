"""
Tests for string matchers
"""
from jestspectation import StringMatchingRegex


def test_bad_type():
    assert StringMatchingRegex('hello*') != 1


def test_match():
    assert StringMatchingRegex('hello*') == 'hello world'


def test_no_match():
    assert StringMatchingRegex('hello*') != 'goodbye world'


def test_diff_match():
    assert StringMatchingRegex('hello*').get_diff('hello world') is None


def test_diff_no_match():
    assert StringMatchingRegex('hello*').get_diff('goodbye world') == [
        "Expected StringMatchingRegex('hello*'), but got 'goodbye world'"
    ]


def test_diff_bad_type():
    assert StringMatchingRegex('hello*').get_diff(1) == [
        "Expected StringMatchingRegex('hello*'), but got int (1)"
    ]
