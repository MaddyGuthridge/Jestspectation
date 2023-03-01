"""
Tests for LinesLike matcher
"""
from jestspectation import LinesLike


def test_incorrect_type():
    assert LinesLike("Hello\nworld") != 12


def test_match_str():
    assert LinesLike("Hello\nworld") == "Hello\nworld"


def test_match_list_self():
    assert LinesLike("Hello\nworld") == ["Hello", "world"]


def test_match_list_other():
    assert LinesLike("Hello\nworld") == ["Hello", "world"]


def test_skip_empty_lines_self():
    assert LinesLike("Hello\n\nworld") == "Hello\nworld"


def test_skip_empty_lines_other():
    assert LinesLike("Hello\nworld") == "Hello\n\nworld"


def test_strip_lines():
    assert LinesLike("Hello\nworld") == " Hello \n world  "


def test_no_match_missing():
    assert LinesLike("Hello\nworld") != "Hello"


def test_no_match_extra():
    assert LinesLike("Hello") != "Hello\nworld"


def test_no_match_different():
    assert LinesLike("Hello") != "Goodbye"


def test_diff_extra_line():
    assert LinesLike("Hello\nworld").get_diff("Hello\nworld\ntest", False) == [
        "LinesLike(['Hello', 'world']) == 'Hello\\nworld\\ntest'",
        "Lines failed to match",
        "== [0] Hello",
        "== [1] world",
        "++ [2] test",
    ]


def test_diff_missing_line():
    assert LinesLike("Hello\nworld\ntest").get_diff("Hello\nworld", False) == [
        "LinesLike(['Hello', 'world', 'test']) == 'Hello\\nworld'",
        "Lines failed to match",
        "== [0] Hello",
        "== [1] world",
        "-- [2] test",
    ]


def test_diff_unequal_line():
    assert LinesLike("Hello\nworld").get_diff("Goodbye\nworld", False) == [
        "LinesLike(['Hello', 'world']) == 'Goodbye\\nworld'",
        "Lines failed to match",
        "!! [0] TextLike('Hello') == 'Goodbye'",
        "   String failed to match",
        "   Expected TextLike('Hello')",
        "   Received 'Goodbye'",
        "== [1] world",
    ]
