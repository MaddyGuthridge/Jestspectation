"""
Tests / Float Approx Test
"""
import pytest
from jestspectation import FloatApprox


def test_magnitude():
    assert 0.1 == FloatApprox(0.2, magnitude=0.1)


def test_magnitude_fail():
    assert 0.1 != FloatApprox(0.21, magnitude=0.1)


def test_percent():
    assert 110 == FloatApprox(100, percent=10)


def test_percent_fail():
    assert 111 != FloatApprox(100, percent=10)


def test_both():
    with pytest.raises(ValueError):
        FloatApprox(100, magnitude=5, percent=10)


def test_divide_by_zero_avoided():
    with pytest.raises(ValueError):
        FloatApprox(0, percent=10)


def test_both_unspecified():
    with pytest.raises(ValueError):
        FloatApprox(10)


def test_get_diff_invalid_type():
    assert FloatApprox(10, magnitude=1).get_diff("my string", False) == [
        "Type mismatch",
        "Expected FloatApprox(10, magnitude=1)",
        "Received object of type str",
    ]


def test_lower_bound_diff():
    assert FloatApprox(10, magnitude=1).get_diff(8, False) == [
        "Value out of range",
        "Expected FloatApprox(10, magnitude=1)",
        "8 is outside lower bound (9)",
    ]


def test_upper_bound_diff():
    assert FloatApprox(10, magnitude=1).get_diff(12, False) == [
        "Value out of range",
        "Expected FloatApprox(10, magnitude=1)",
        "12 is outside upper bound (11)",
    ]
