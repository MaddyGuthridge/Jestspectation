"""
Logicals

Matchers that can be used to perform logical operations on other matchers
"""
from .__jestspectation_base import JestspectationBase
from .__util import sub_diff_delegate


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

    def get_diff(self, other: object) -> list[str]:
        ret = [
            "Not all matches fulfilled",
            f"Object {repr(other)} failed to match with",
        ]
        for m in self.__get_misses(other):
            diff = sub_diff_delegate(m, other)
            assert diff is not None
            diff[0] = '-- ' + diff[0][3:]
            ret += diff

        return ret


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

    def get_diff(self, other: object) -> list[str]:
        ret = [
            "No matches fulfilled",
            f"Object {repr(other)} must match with at least one of",
        ]
        for m in self.__matchers:
            diff = sub_diff_delegate(m, other)
            assert diff is not None
            diff[0] = '-- ' + diff[0][3:]
            ret += diff

        return ret


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

    def get_diff(self, other: object) -> list[str]:
        hits = self.__get_hits(other)
        if len(hits) == 0:
            ret = [
                "No matches fulfilled",
                f"Object {repr(other)} must match with at least one of",
            ]
            for m in self.__matchers:
                diff = sub_diff_delegate(m, other)
                assert diff is not None
                diff[0] = '-- ' + diff[0][3:]
                ret += diff
        else:
            ret = [
                "Too many matches fulfilled",
                f"Object {repr(other)} matched with",
            ]
            for m in hits:
                diff = sub_diff_delegate(m, other)
                assert diff is not None
                diff[0] = '++ ' + diff[0][3:]
                ret += diff
            ret += [
                "But should only have matched with one of them",
            ]
        return ret
