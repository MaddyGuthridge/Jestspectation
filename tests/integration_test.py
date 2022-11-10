"""
Tests / integration test

Tests that emulate the expected usage of Jestspectation
"""
import jestspectation as expect


def test_basic_dict_match():
    assert {
        "a": 1,
        "b": 2,
        "c": 3,
    } == {
        "a": 1,
        "b": expect.Any(int),
        "c": expect.FloatApprox(2.5, magnitude=0.5)
    }


def test_nested_match():
    assert {
        "my_dict": {
            "a": 1,
            "b": "Jazz",
        },
        "my_list": [1, 2, 3],
    } == {
        "my_dict": expect.DictContainingItems({
            "b": expect.Any(str)
        }),
        "my_list": expect.ListContaining([3]),
    }
