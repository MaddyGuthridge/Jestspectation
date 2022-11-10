from typing import Optional


class FloatApprox:
    """
    Float approximately equal
    """
    def __init__(
        self,
        value: float,
        magnitude: Optional[float] = None,
        percent: Optional[float] = None,
    ) -> None:
        if magnitude is None and percent is None:
            raise ValueError("Magnitude or percent must be specified")
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
