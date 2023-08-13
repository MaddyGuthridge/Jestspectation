"""
Matcher for floats of approximate value
"""
from typing import Optional
from .__jestspectation_base import JestspectationBase


class FloatApprox(JestspectationBase):
    """
    Float approximately equal
    """
    def __init__(
        self,
        value: float,
        magnitude: Optional[float] = None,
        percent: Optional[float] = None,
    ) -> None:
        """
        Float approximately equal.

        Args:
            value (float): target value.
            magnitude (Optional[float], optional): maximum magnitude
                difference. Defaults to None.
            percent (Optional[float], optional): maximum percentage difference.
                Percentage differences are always calculated based on the
                expected value, regardless of ordering. Defaults to None.

        If both a magnitude and percent are specified, both will be checked.

        Raises:
            ValueError: At least one of magnitude or percent must be specified
            ValueError: Cannot calculate a percentage difference from 0
        """
        if magnitude is None and percent is None:
            raise ValueError(
                "One of magnitude or percent must be specified")
        if magnitude is not None and percent is not None:
            raise ValueError(
                "Only one of magnitude or percent can be specified")
        if percent is not None and value == 0:
            raise ValueError("Cannot calculate a percentage difference from 0")
        self.__value = value
        self.__magnitude = magnitude
        self.__percent = percent

    def boundary_width(self) -> float:
        """
        Returns the width of the boundary with the float.

        Any value that is between `value-width` and `value+width` will match.
        """
        if self.__magnitude is not None:
            return self.__magnitude
        else:
            assert self.__percent is not None
            return self.__value * self.__percent / 100

    def __repr__(self) -> str:
        if self.__percent is None:
            return f"FloatApprox({self.__value}, magnitude={self.__magnitude})"
        elif self.__magnitude is None:
            return f"FloatApprox({self.__value}, percent={self.__percent})"
        else:
            return (
                f"FloatApprox({self.__value}, "
                f"magnitude={self.__magnitude}, "
                f"percent={self.__percent})"
            )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, (float, int)):
            return False
        diff_magnitude = abs(self.__value - other)
        if self.__magnitude is not None:
            if diff_magnitude > self.__magnitude:
                return False
        if self.__percent is not None:
            diff_percent = diff_magnitude / self.__value * 100
            if diff_percent > self.__percent:
                return False
        return True

    def get_diff(self, other, other_is_lhs: bool) -> list[str]:
        if not isinstance(other, (int, float)):
            head = "Type mismatch"
            err = f"Received object of type {type(other).__name__}"
        elif other < self.__value:
            lower = self.__value - self.boundary_width()
            head = "Value out of range"
            err = f"{repr(other)} is outside lower bound ({lower})"
        else:
            upper = self.__value + self.boundary_width()
            head = "Value out of range"
            err = f"{repr(other)} is outside upper bound ({upper})"
        return [
            head,
            f"Expected {self}",
            err,
        ]
