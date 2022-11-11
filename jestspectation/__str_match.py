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

    def get_diff(self, other) -> Optional[list[str]]:
        if self == other:
            return None
        if not isinstance(other, str):
            return [
                f"Expected {repr(self)}, but got "
                f"{type(other).__name__} ({other})"
            ]
        else:
            return [f"Expected {repr(self)}, but got {repr(other)}"]
