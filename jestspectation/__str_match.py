"""
Matchers for strings
"""
import re
from typing import Optional
from .__jestspectation_base import JestspectationBase


class StringMatchingRegex(JestspectationBase):
    def __init__(self, regex: str) -> None:
        self.__raw_regex = regex
        self.__regex = re.compile(regex)

    def __repr__(self) -> str:
        return f"StringMatchingRegex({repr(self.__raw_regex)})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, str):
            return False
        return re.match(self.__regex, other) is not None

    def get_diff(self, other: object) -> Optional[list[str]]:
        if self == other:
            return None
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
