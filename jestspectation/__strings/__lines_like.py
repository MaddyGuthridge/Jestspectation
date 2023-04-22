"""
Matches text similar to the given text, but with better diffs for
multi-line text
"""
from itertools import zip_longest
from typing import Union, overload, Optional, Iterable

from .__text_like import TextLike
from ..__jestspectation_base import JestspectationBase
from ..__util import sub_diff_delegate, safe_diff_wrapper


class LinesLike(JestspectationBase):
    """
    Matches text similar to the given text, but can display diffs of multiple
    lines. Empty lines are ignored.
    """

    def __create_match_list(self, lines: list[str]) -> list[TextLike]:
        """
        Filter lines so that we're only trying to match lines containing
        content
        """
        new_lines = []
        for line in lines:
            if self.__strip_lines:
                line = line.strip()
            if line == "":
                continue
            new_lines.append(TextLike(
                line,
                ignore_case=self.__ignore_case,
                ignored_sequences=self.__ignored_sequences
            ))
        return new_lines

    def __filter_lines(self, lines: list[str]) -> list[str]:
        new_lines = []
        for line in lines:
            if self.__strip_lines:
                line = line.strip()
            if line == "":
                continue
            new_lines.append(line)
        return new_lines

    @overload
    def __init__(
        self,
        lines: list[str],
        /,
        ignore_case: bool = True,
        ignored_sequences: Optional[Iterable[str]] = None,
        strip_lines: bool = False,
    ) -> None:
        ...

    @overload
    def __init__(
        self,
        lines: str,
        /,
        ignore_case: bool = True,
        ignored_sequences: Optional[Iterable[str]] = None,
        strip_lines: bool = False,
    ) -> None:
        ...

    def __init__(
        self,
        lines: Union[list[str], str],
        /,
        ignore_case: bool = True,
        ignored_sequences: Optional[Iterable[str]] = None,
        strip_lines: bool = False,
    ) -> None:
        """
        Matches text similar to the given text, but can display diffs of
        multiple lines. Empty lines are ignored.

        Args:
            lines (list[str]): text to match
            ignore_case (bool, optional): whether to ignore the case of
                characters. Defaults to True.
            ignored_sequences (Optional[Iterable[str]], optional): sequences
                of characters to ignore in the string. Defaults to None.
            strip_lines (bool, optional): whether to strip each line before
                processing. Defaults to False.
        """
        if isinstance(lines, str):
            lines = lines.splitlines()

        self.__ignore_case = ignore_case
        self.__strip_lines = strip_lines
        self.__ignored_sequences = ignored_sequences

        self.__og_lines = lines
        self.__lines = self.__create_match_list(lines)

    def __repr__(self) -> str:
        return f"LinesLike({repr(self.__og_lines)})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            lines = self.__filter_lines(other.splitlines())
        elif isinstance(other, list):
            lines = self.__filter_lines(other)
        else:
            return False

        if len(lines) != len(self.__lines):
            return False

        return all([
            actual == expected
            for actual, expected in zip(lines, self.__lines)
        ])

    @safe_diff_wrapper
    def get_diff(self, other: object, other_is_lhs: bool) -> list[str]:
        if isinstance(other, str):
            lines = self.__filter_lines(other.splitlines())
        elif isinstance(other, list):
            lines = self.__filter_lines(other)
        else:
            return [
                "Type mismatch",
                f"Expected object of type str ({repr(self)})",
                f"Received object of type {type(other).__name__} ({other})"
            ]

        # Generate the diffs for each line
        diffs: list[str] = []

        for i, (expected, actual) in enumerate(
            zip_longest(self.__lines, lines)
        ):
            if expected == actual:
                diffs.append(f"== [{i}] {expected}")
            elif expected is None:
                diffs.append(f"++ [{i}] {actual}")
            elif actual is None:
                diffs.append(f"-- [{i}] {expected}")
            else:
                sub_diff = sub_diff_delegate(expected, actual, other_is_lhs)
                assert sub_diff is not None
                sub_diff[0] = f"!! [{i}] {sub_diff[0][3:]}"
                diffs.extend(sub_diff)

        return [
            "Lines failed to match",
        ] + diffs
