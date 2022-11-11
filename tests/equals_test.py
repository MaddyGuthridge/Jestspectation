"""
Equals test
"""
from jestspectation import Is


def test_is_exact():
    arr = [1, 2, 3, 4, 5]
    assert Is(arr) == arr


def test_is_not():
    assert Is([1, 2, 3, 4, 5]) != [1, 2, 3, 4]


def test_diff_is():
    arr = [1, 2, 3, 4, 5]
    assert Is(arr).get_diff(arr) is None


def test_diff_is_not():
    l1 = [1, 2, 3, 4, 5]
    l2 = [1, 2, 3, 4]
    assert Is(l1).get_diff(l2) == [
        "Object identities not equal",
        f"Expected {l1} with id {id(l1)}",
        f"Received {l2} with id {id(l2)}",
    ]


def test_diff_is_not_but_equal():
    """
    Special case - give extra help if the objects are equal, but have different
    IDs
    """
    l1 = [1, 2, 3, 4, 5]
    l2 = [1, 2, 3, 4, 5]
    assert Is(l1).get_diff(l2) == [
        "Object identities not equal",
        f"Expected {l1} with id {id(l1)}",
        f"Received {l2} with id {id(l2)}",
        "Note that although these values are equal, they have "
        "different identifiers, meaning their memory addresses are "
        "different",
    ]
