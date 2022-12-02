"""
Equals

Matches for types of equality
"""
from .__jestspectation_base import JestspectationBase
from .__util import sub_diff_delegate


class Is(JestspectationBase):
    """
    Matches values that have the same identity as the given value.

    While this isn't as useful for top-level comparisons, it can be used
    effectively for checking nested data structures.
    """
    def __init__(self, value: object) -> None:
        """
        Matches values that have the same identity as the given value.

        Args:
            value (object): object to check
        """
        self.__value = value

    def __repr__(self) -> str:
        return f"Is({self.__value})"

    def __eq__(self, other: object) -> bool:
        return self.__value is other

    def get_diff(self, other: object, other_is_lhs: bool) -> list[str]:
        # Give a more helpful error if the objects are equal but have different
        # identities
        return [
            f"{repr(self.__value)} is {repr(other)}",
            "Object identities not equal",
            f"Expected {repr(self.__value)} with id {id(self.__value)}",
            f"Received {repr(other)} with id {id(other)}",
        ] + (
            [
                "Note that although these values are equal, they have "
                "different identifiers, meaning their memory addresses are "
                "different"
            ]
            if self.__value == other
            else []
        )


class Equals(JestspectationBase):
    """
    Matches objects that have the same value.

    This is equivalent to the `==` operator, but with additional information
    on the difference, which can help with debugging.
    """
    def __init__(self, value: object) -> None:
        """
        Matches values that have the same identity as the given value.

        Args:
            value (object): object to check
        """
        self.__value = value

    def __repr__(self) -> str:
        return f"Equals({self.__value})"

    def __eq__(self, other: object) -> bool:
        return self.__value == other

    def get_diff(self, other: object, other_is_lhs: bool) -> list[str]:
        # Give a more helpful error if the objects are equal but have different
        # identities
        diff = sub_diff_delegate(
            self.__value,
            other,
            other_is_lhs,
            indent=False,
        )
        assert diff is not None
        return diff
