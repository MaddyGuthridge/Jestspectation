"""
Tests for string matchers
"""

from jestspectation import StringMatchingRegex


def test_bad_type():
    assert StringMatchingRegex("hello*") != 1


def test_match():
    assert StringMatchingRegex("hello*") == "hello world"


def test_no_match():
    assert StringMatchingRegex("hello*") != "goodbye world"


def test_diff_no_match():
    assert StringMatchingRegex("hello*").get_diff("goodbye world", False) == [
        "StringMatchingRegex('hello*') == 'goodbye world'",
        "Regex failed to match",
        "Expected StringMatchingRegex('hello*')",
        "Received 'goodbye world'",
    ]


def test_diff_bad_type():
    assert StringMatchingRegex("hello*").get_diff(1, False) == [
        "StringMatchingRegex('hello*') == 1",
        "Type mismatch",
        "Expected object of type str (StringMatchingRegex('hello*'))",
        "Received object of type int (1)",
    ]
