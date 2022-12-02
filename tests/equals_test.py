"""
Equals test
"""
from jestspectation import Is, Equals


def test_is_exact():
    arr = [1, 2, 3, 4, 5]
    assert Is(arr) == arr


def test_is_not():
    assert Is([1, 2, 3, 4, 5]) != [1, 2, 3, 4]


def test_diff_is_not():
    l1 = [1, 2, 3, 4, 5]
    l2 = [1, 2, 3, 4]
    assert Is(l1).get_diff(l2, False) == [
        "[1, 2, 3, 4, 5] is [1, 2, 3, 4]",
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
    assert Is(l1).get_diff(l2, False) == [
        "[1, 2, 3, 4, 5] is [1, 2, 3, 4, 5]",
        "Object identities not equal",
        f"Expected {l1} with id {id(l1)}",
        f"Received {l2} with id {id(l2)}",
        "Note that although these values are equal, they have "
        "different identifiers, meaning their memory addresses are "
        "different",
    ]


def test_equals():
    """
    Test that equal values are equal
    """
    assert Equals({'a': 1, 'b': 2, 'c': 3}) == {'a': 1, 'b': 2, 'c': 3}


def test_not_equals():
    """
    Test that non-equal values are not equal
    """
    assert Equals({'a': 1, 'b': 2, 'c': 3}) != {'a': 1, 'b': 2, 'c': 2}


def test_diff_equals():
    """
    Test diff for the Equals matcher
    """
    eq = Equals({'a': 1, 'b': 2, 'c': 3})
    diff = eq.get_diff({'a': 1, 'b': 2, 'c': 2}, False)
    assert diff == [
        "{'a': 1, 'b': 2, 'c': 3} == {'a': 1, 'b': 2, 'c': 2}",
        "!! 'c': 3 == 'c': 2",
        "   3 == 2",
        "   Value mismatch",
        "   Expected 3",
        "   Received 2",
    ]
