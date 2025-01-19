from jestspectation import ObjectContainingItems, ObjectContainingProperties


class DummyObject:
    """A dummy object for testing purposes"""

    def __init__(self, a, b, c) -> None:
        self.a = a
        self.b = b
        self.c = c

    def __repr__(self) -> str:
        return f"DummyObject({self.a}, {self.b}, {self.c})"


def test_object_property_matches():
    assert DummyObject(1, 2, 3) == ObjectContainingProperties({"a", "b", "c"})


def test_object_property_missing():
    assert DummyObject(1, 2, 3) != ObjectContainingProperties({"a", "b", "d"})


def test_diff_match_object_containing_props():
    obj = ObjectContainingProperties({"a", "d"})
    assert obj.get_diff(DummyObject(1, 2, 3), False) == [
        "ObjectContainingProperties(a, d) == DummyObject(1, 2, 3)",
        "Missing properties",
        f"Expected a {obj}",
        "-- d",
    ]


def test_object_item_matches():
    assert DummyObject(1, 2, 3) == ObjectContainingItems(
        {
            "a": 1,
            "b": 2,
            "c": 3,
        }
    )


def test_object_item_missing():
    assert DummyObject(1, 2, 3) != ObjectContainingItems(
        {
            "a": 1,
            "b": 2,
            "d": 4,
        }
    )


def test_object_item_not_equal():
    assert DummyObject(1, 2, 3) != ObjectContainingItems(
        {
            "a": 1,
            "b": 2,
            "c": 4,
        }
    )


def test_diff_missing_object_containing_props():
    obj = ObjectContainingItems({"a": 1, "d": 4})
    assert obj.get_diff(DummyObject(1, 2, 3), False) == [
        "ObjectContainingItems(a = 1, d = 4) == DummyObject(1, 2, 3)",
        "Missing properties",
        f"Expected a {obj}",
        "-- d = 4",
    ]


def test_diff_incorrect_object_containing_props():
    obj = ObjectContainingItems({"a": 1, "c": 4})
    assert obj.get_diff(DummyObject(1, 2, 3), False) == [
        "ObjectContainingItems(a = 1, c = 4) == DummyObject(1, 2, 3)",
        "Incorrect properties",
        f"Expected a {obj}",
        "!! c = 4 == c = 3",
        "   4 == 3",
        "   Value mismatch",
        "   Expected 4",
        "   Received 3",
    ]
