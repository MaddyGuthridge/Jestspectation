"""
Logicals / And

Matchers that can be used to perform logical operations on other matchers
"""
from ..__jestspectation_base import JestspectationBase
from ..__util import sub_diff_delegate, safe_diff_wrapper


class And(JestspectationBase):
    """
    Match all of the given matchers
    """

    def __init__(self, *matchers: object) -> None:
        """
        Match all of the given matchers

        For example:

        ```py
        # Matches any string that doesn't match with the
        # regex "hello*"
        And(Any(str), Not(StringMatchingRegex("hello*")))
        ```

        Args:
            matchers (object): matchers to use
        """
        if len(matchers) < 2:
            raise TypeError(
                "At least two matchers are required for an And matcher")
        self.__matchers = matchers

    def __repr__(self) -> str:
        return f"And{repr(self.__matchers)}"

    def __eq__(self, other: object) -> bool:
        return len(self.__get_misses(other)) == 0

    def __get_misses(self, other: object) -> list[object]:
        """
        Return matchers that didn't match
        """
        return list(filter(
            lambda m: m != other,
            self.__matchers
        ))

    @safe_diff_wrapper
    def get_diff(self, other: object, other_is_lhs: bool) -> list[str]:
        ret = [
            "Not all matches fulfilled",
            f"{repr(other)} failed to match with",
        ]
        for m in self.__get_misses(other):
            diff = sub_diff_delegate(m, other, other_is_lhs)
            assert diff is not None
            diff[0] = '-- ' + diff[0][3:]
            ret += diff

        return ret
