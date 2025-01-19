"""
Tests for smart representations of items
"""

from jestspectation import ListContaining


def test_single_element():
    """Normal representation with single element"""
    assert repr(ListContaining([1])) == "ListContaining([1])"


def test_normal_representation():
    """Normal representation with no trimming"""
    assert repr(ListContaining([1, 2, 3])) == "ListContaining([1, 2, 3])"


def test_last_element_barely_fits():
    """Last element of the list barely fits in repr"""
    assert (
        repr(ListContaining([1, 2, 3, 4, 5, 6, 7, 10]))
        == "ListContaining([1, 2, 3, 4, 5, 6, 7, 10])"
    )


def test_elements_trimmed():
    """Later elements get trimmed if they're too long"""
    assert (
        repr(ListContaining([1, 2, 3, 4, 5, 6, 7, 8, 9]))
        == "ListContaining([1, 2, 3, 4, 5, 6, 7, ...])"
    )


def test_no_elements_fit():
    """Later elements get trimmed if they're too long"""
    assert (
        repr(ListContaining(["1234567890123456789012345"]))
        == "ListContaining([...])"
    )
