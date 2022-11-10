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
    assert 109 != FloatApprox(100, magnitude=5, percent=10)
    assert 109 != FloatApprox(100, magnitude=10, percent=5)
    assert 109 == FloatApprox(100, magnitude=10, percent=10)


def test_divide_by_zero_avoided():
    with pytest.raises(ValueError):
        FloatApprox(0, percent=10)


def test_both_unspecified():
    with pytest.raises(ValueError):
        FloatApprox(10)
