"""
Tests / integration test

Tests that emulate the expected usage of Jestspectation
"""
import jestspectation as expect


def test_basic_dict_match():
    assert {
        "a": 1,
        "b": expect.Any(int),
        "c": expect.FloatApprox(2.5, magnitude=0.5)
    } == {
        "a": 1,
        "b": 2,
        "c": 3,
    }


def test_nested_match():
    assert {
        "my_dict": expect.DictContainingItems({
            "b": expect.Any(str)
        }),
        "my_list": expect.ListContaining([3]),
    } == {
        "my_dict": {
            "a": 1,
            "b": "Jazz",
        },
        "my_list": [1, 2, 3],
    }


def test_advanced():
    my_dict = {
        "foo": "Hello",
        "bar": 1.002,
        "baz": [
            {
                "this": 1,
                "shouldn't": 2,
                "match": 3,
            },
            {
                "some_value": True,
                "other_value": "Hello",
                "yet_another_value": {
                    "contents": 42,
                    "more_contents": "Hello",
                }
            }
        ]
    }
    expected = expect.DictContainingItems({
        "foo": expect.Any(str),
        "bar": expect.FloatApprox(1, percent=1),
        "baz": expect.ListContaining([{
            "some_value": expect.Any(bool),
            "other_value": "Hello",
            "yet_another_value": {
                "contents": expect.Any(int),
                "more_contents": expect.Not(
                    expect.StringMatchingRegex("Goodbye*"))
            }
        }])
    })
    assert expected == my_dict
