import pytest

from jestspectation import Equals, assert_eq


def test_assert_eq_success():
    assert_eq(1, 1)


def test_raises_assertion_error():
    with pytest.raises(AssertionError):
        assert_eq(1, 2)


def test_gives_diff():
    try:
        assert_eq(1, 2)
    except AssertionError as e:
        assert e.args == ('\n'.join(Equals(1).get_diff(2, False)),)
