"""
Logicals / Or

Matchers that can be used to perform logical operations on other matchers
"""
from ..__jestspectation_base import JestspectationBase
from ..__util import sub_diff_delegate, safe_diff_wrapper


class Or(JestspectationBase):
    """
    Match at least one of the given matchers
    """

    def __init__(self, *matchers: object) -> None:
        """
        Match at least one of the given matchers

        For example:

        ```py
        # Matches any object that is a str or int
        Or(Any(str), Any(int))
        ```

        Args:
            matchers (object): matchers to use
        """
        if len(matchers) < 2:
            raise TypeError(
                "At least two matchers are required for an Or matcher")
        self.__matchers = matchers

    def __repr__(self) -> str:
        return f"Or{repr(self.__matchers)}"

    def __eq__(self, other: object) -> bool:
        return len(self.__get_hits(other)) > 0

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
        ret = [
            "No matches fulfilled",
            f"{repr(other)} must match with at least one of",
        ]
        for m in self.__matchers:
            diff = sub_diff_delegate(m, other, other_is_lhs)
            assert diff is not None
            diff[0] = '-- ' + diff[0][3:]
            ret += diff

        return ret
