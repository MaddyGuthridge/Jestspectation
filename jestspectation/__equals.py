"""
Equals

Matches for types of equality
"""
from typing import Optional
from .__jestspectation_base import JestspectationBase


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

    def get_diff(self, other: object) -> Optional[list[str]]:
        if self == other:
            return None
        # Give a more helpful error if the objects are equal but have different
        # identities
        return [
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
