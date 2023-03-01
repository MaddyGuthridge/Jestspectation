"""
Matches text similar to the given text
"""
from typing import Optional, Iterable

from ..__jestspectation_base import JestspectationBase
from ..__util import safe_diff_wrapper


class TextLike(JestspectationBase):
    """
    Matches text similar to the given text.

    Can ignore case, and sequences of characters.
    """
    def __simplify_text(self, text: str) -> str:
        if self.__strip:
            text = text.strip()
        if self.__ignore_case:
            text = text.casefold()
        for seq in self.__ignored_sequences:
            text = text.replace(seq, "")
        return text

    def __init__(
        self,
        text: str,
        /,
        ignore_case: bool = True,
        ignored_sequences: Optional[Iterable[str]] = None,
        strip: bool = False,
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
            strip (bool, optional): whether to strip the text before
                processing. Defaults to False.
        """
        self.__og_text = text
        self.__ignore_case = ignore_case
        self.__strip = strip
        if ignored_sequences is None:
            self.__ignored_sequences: Iterable[str] = []
        else:
            self.__ignored_sequences = ignored_sequences

        self.__match_text = self.__simplify_text(self.__og_text)

    def __repr__(self) -> str:
        return f"TextLike({repr(self.__og_text)})"

    def __str__(self) -> str:
        return self.__og_text

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
