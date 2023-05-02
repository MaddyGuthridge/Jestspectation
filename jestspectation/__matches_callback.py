"""
Matches callback

Match values based on a callback
"""
from typing import Callable
import inspect
from .__jestspectation_base import JestspectationBase


class MatchesCallback(JestspectationBase):
    """
    Matches values based on a callback
    """
    def __init__(self, callback: Callable[[object], bool]) -> None:
        """
        Matches values when a callback returns True

        Args:
            callback (Callable[[object], bool]): callback used to check the
            given value.
        """
        if not callable(callback):
            raise TypeError("callback must be callable")
        self.__callback = callback

    def __callback_str(self) -> str:
        """
        Return the first line of the callback
        """
        return inspect.getsource(self.__callback)

    def __repr__(self) -> str:
        return f"MatchesLambda({self.__callback_str()})"

    def __eq__(self, other: object) -> bool:
        return self.__callback(other)

    def get_diff(self, other: object, other_is_lhs: bool) -> list[str]:
        try:
            _ = self == other
        except Exception as e:
            return [
                f"{repr(self)} on {other}",
                f"Callback raised a {type(e).__name__}",
                f"Expected {self.__callback_str()} to return True",
                f"But given {other}, it raised the exception",
                f"{e}",
            ]
        return [
            f"{repr(self)} on {other}",
            "Callback did not return True for object",
            f"Expected {self.__callback_str()} to return True",
            f"But given {other}, it returned False",
        ]
