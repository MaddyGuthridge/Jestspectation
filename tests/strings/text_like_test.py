"""
Tests for string matchers
"""
from jestspectation import TextLike
from string import whitespace


def test_bad_type():
    assert TextLike('hello') != 1


def test_match():
    assert TextLike('hello') == 'HELLO'


def test_disable_casefold():
    assert TextLike('hello', ignore_case=False) != 'HELLO'


def test_ignore_spacing():
    assert TextLike('hello  world', ignored_sequences=whitespace)\
        == "hello\tworld"


def test_strip():
    assert TextLike('hello', strip=True) == '  hello\n '


def test_no_match():
    assert TextLike('hello') != 'goodbye'


def test_diff_no_match():
    assert TextLike('hello').get_diff('goodbye', False) == [
        "TextLike('hello') == 'goodbye'",
        "String failed to match",
        "Expected TextLike('hello')",
        "Received 'goodbye'",
    ]


def test_diff_bad_type():
    assert TextLike('hello').get_diff(1, False) == [
        "TextLike('hello') == 1",
        "Type mismatch",
        "Expected object of type str (TextLike('hello'))",
        "Received object of type int (1)",
    ]
