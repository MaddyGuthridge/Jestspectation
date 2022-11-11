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
            Percentage differences are always calculated based on the expected
            value, regardless of ordering. Defaults to None.

        If both a magnitude and percent are specified, both will be checked.

        Raises:
            ValueError: At least one of magnitude or percent must be specified
            ValueError: Cannot calculate a percentage difference from 0
        """
        if magnitude is None and percent is None:
            raise ValueError(
                "At least one of magnitude or percent must be specified")
        if percent is not None and value == 0:
            raise ValueError("Cannot calculate a percentage difference from 0")
        self.__value = value
        self.__magnitude = magnitude
        self.__percent = percent

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

    def get_diff(self, other) -> Optional[list[str]]:
        if self == other:
            return None
        if not isinstance(other, (int, float)):
            err = f"But got {type(other).__name__}"
        elif other < self.__value:
            err = f"{repr(other)} is outside lower bound"
        else:
            err = f"{repr(other)} is outside upper bound"
        return [
            f"Expected {repr(other)} to be {self}",
            f"   {err}",
        ]
