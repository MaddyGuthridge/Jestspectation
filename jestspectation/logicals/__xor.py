"""
Logicals / Xor

Matchers that can be used to perform logical operations on other matchers
"""
from ..__jestspectation_base import JestspectationBase
from ..__util import sub_diff_delegate, safe_diff_wrapper


class Xor(JestspectationBase):
    """
    Match exactly one of the given matchers
    """

    def __init__(self, *matchers: object) -> None:
        """
        Match exactly one of the given matchers

        For example:

        ```py
        # Matches any object that is a str or int, but not both
        # Yes I know this a bit of a bad example, but I can't come up with
        # anything right now ok
        Xor(Any(str), Any(int))
        ```

        Args:
            matchers (object): matchers to use
        """
        if len(matchers) < 2:
            raise TypeError(
                "At least two matchers are required for an Xor matcher")
        self.__matchers = matchers

    def __repr__(self) -> str:
        return f"Xor{repr(self.__matchers)}"

    def __eq__(self, other: object) -> bool:
        return len(self.__get_hits(other)) == 1

    def __get_hits(self, other: object) -> list[object]:
        """
        Return matchers that matched
        """
        return list(filter(
            lambda m: m == other,
            self.__matchers
        ))

    @safe_diff_wrapper
    def get_diff(self, other: object, other_is_lhs: bool) -> list[str]:
        hits = self.__get_hits(other)
        if len(hits) == 0:
            ret = [
                "No matches fulfilled",
                f"{repr(other)} must match with exactly one of",
            ]
            for m in self.__matchers:
                diff = sub_diff_delegate(m, other, other_is_lhs)
                assert diff is not None
                diff[0] = '-- ' + diff[0][3:]
                ret += diff
        else:
            ret = [
                "Too many matches fulfilled",
                f"{repr(other)} matched with",
            ]
            for m in hits:
                ret += [f"++ {repr(m)} == {repr(other)}"]
            ret += [
                "But should only have matched with one of them",
            ]
        return ret
