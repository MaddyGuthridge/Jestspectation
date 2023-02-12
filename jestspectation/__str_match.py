"""
Matchers for strings
"""
import re
from typing import Iterable, Optional
from .__jestspectation_base import JestspectationBase
from .__util import safe_diff_wrapper


class StringMatchingRegex(JestspectationBase):
    """
    Matches strings that match with the given regular expression.
    """
    def __init__(self, regex: str) -> None:
        """
        Matches strings that match with the given regular expression.

        Args:
            regex (str): regular expression to match against
        """
        self.__raw_regex = regex
        self.__regex = re.compile(regex)

    def __repr__(self) -> str:
        return f"StringMatchingRegex({repr(self.__raw_regex)})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, str):
            return False
        return re.match(self.__regex, other) is not None

    @safe_diff_wrapper
    def get_diff(self, other: object, other_is_lhs: bool) -> list[str]:
        if not isinstance(other, str):
            return [
                "Type mismatch",
                f"Expected object of type str ({repr(self)})",
                f"Received object of type {type(other).__name__} ({other})"
            ]
        else:
            return [
                "Regex failed to match",
                f"Expected {repr(self)}",
                f"Received {repr(other)}",
            ]


class StringContaining(JestspectationBase):
    """
    Matches any string that contains the given substring
    """
    def __init__(self, substring: str) -> None:
        """
        Matches any string that contains the given substring

        Args:
            substring (str): string that should be contained within other
                object
        """
        self.__substring = substring

    def __repr__(self) -> str:
        return f"StringContaining({repr(self.__substring)})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, str):
            return False
        return self.__substring in other

    @safe_diff_wrapper
    def get_diff(self, other: object, other_is_lhs: bool) -> list[str]:
        if not isinstance(other, str):
            return [
                "Type mismatch",
                f"Expected object of type str ({repr(self)})",
                f"Received object of type {type(other).__name__} ({other})"
            ]
        else:
            return [
                "String failed to match",
                f"Expected {repr(self)}",
                f"Received {repr(other)}",
            ]


class TextLike(JestspectationBase):
    """
    Matches text similar to the given text.

    Can ignore case, and sequences of characters.
    """
    def __simplify_text(self, text: str) -> str:
        if self.__ignore_case:
            text = text.casefold()
        for seq in self.__ignored_sequences:
            text = text.replace(seq, "")
        return text

    def __init__(
        self,
        text: str,
        ignore_case: bool = True,
        ignored_sequences: Optional[Iterable[str]] = None
    ) -> None:
        """
        Matches text that is similar to the given text.

        Can ignore case, and sequences of characters.

        Args:
            text (str): text to match
            ignore_case (bool, optional): whether to ignore the case of
                characters. Defaults to True.
            ignored_sequences (Optional[Iterable[str]], optional): sequences
                of characters to ignore in the string. Defaults to None.
        """
        self.__text = text
        self.__ignore_case = ignore_case
        if ignored_sequences is None:
            self.__ignored_sequences: Iterable[str] = []
        else:
            self.__ignored_sequences = ignored_sequences

        self.__match_text = self.__simplify_text(self.__text)

    def __repr__(self) -> str:
        return f"TextLike({repr(self.__text)})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, str):
            return False
        return self.__match_text == self.__simplify_text(other)

    @safe_diff_wrapper
    def get_diff(self, other: object, other_is_lhs: bool) -> list[str]:
        if not isinstance(other, str):
            return [
                "Type mismatch",
                f"Expected object of type str ({repr(self)})",
                f"Received object of type {type(other).__name__} ({other})"
            ]
        else:
            return [
                "String failed to match",
                f"Expected {repr(self)}",
                f"Received {repr(other)}",
            ]
