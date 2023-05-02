"""
Tests / Matches callback test

Tests for the matches callback matcher
"""
import pytest
from jestspectation import MatchesCallback


def test_basic():
    assert MatchesCallback(lambda x: True) == 42


def test_not_callable():
    with pytest.raises(TypeError):
        MatchesCallback(42)  # type: ignore


@pytest.mark.parametrize(
    ('callback', 'match', 'no_match'),
    [
        (lambda x: x is None, None, True),
        (lambda x: isinstance(x, int), 42, "42"),
    ]
)
def test_simple_cases(callback, match, no_match):
    matcher = MatchesCallback(callback)
    assert matcher == match
    assert matcher != no_match


def test_callback_raises():
    def callback(x):
        raise ValueError("No")
    with pytest.raises(ValueError):
        assert MatchesCallback(callback) == 10


def test_diff_basic():
    assert MatchesCallback(lambda x: False).get_diff(10, False) == [
        'MatchesCallback(lambda x: False) on 10',
        'Callback did not return True for object',
        'Expected lambda x: False to return True',
        'But given 10, it returned False',
    ]
