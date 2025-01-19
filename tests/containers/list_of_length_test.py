import pytest

from jestspectation import ListOfLength


def test_list_of_length():
    assert ListOfLength(3) == [1, 2, 3]


def test_list_of_length_incorrect():
    assert ListOfLength(3) != [1, 2]


def test_list_of_length_invalid_arg():
    with pytest.raises(ValueError):
        ListOfLength(-1)


def test_diff_list_of_length():
    assert ListOfLength(3).get_diff([1, 2], False) == [
        "Length failed to match",
        "Expected list of length 3",
        "Received list of length 2 ([1, 2])",
    ]


def test_diff_invalid_type():
    assert ListOfLength(3).get_diff({}, False) == [
        "Type mismatch",
        "Expected object of type list (ListOfLength(3))",
        "Received object of type dict ({})",
    ]
