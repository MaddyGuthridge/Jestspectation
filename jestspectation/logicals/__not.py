"""
Logicals / Not

Matchers that can be used to perform logical operations on other matchers
"""
from ..__jestspectation_base import JestspectationBase


class Not(JestspectationBase):
    """
    Match the negative of the given matcher
    """

    def __init__(self, matcher: object) -> None:
        """
        Match the negative of the given matcher

        For example:

        ```py
        # Matches anything that isn't a string
        assert 1 == Not(Any(str))
        # Matches anything that is not "nice"
        assert 68 == Not("nice")
        ```

        Args:
            matcher (object): matcher to negate
        """
        self.__matcher = matcher

    def __repr__(self) -> str:
        return f"Not({repr(self.__matcher)})"

    def __eq__(self, object: object) -> bool:
        return not self.__matcher == object

    def get_diff(self, other: object) -> list[str]:
        return [
            "Unwanted match",
            f"Expected object that doesn't match with {repr(self.__matcher)}",
            f"Received {repr(other)}"
        ]
