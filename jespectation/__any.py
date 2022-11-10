# from typing import Typ


class Any:
    """
    Matches any object that is an instance of the given type
    """

    def __init__(self, match_type: type) -> None:
        """
        Matches any object that is an instance of the given type

        Args:
            match_type (type): type to match
        """
        self.__match_type = match_type

    def __repr__(self) -> str:
        return f"Any({self.__match_type.__name__})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__match_type)


class Anything:
    """
    Matches any Python object
    """

    def __init__(self) -> None:
        """
        Matches any Python object
        """

    def __repr__(self) -> str:
        return "Anything()"

    def __eq__(self, other: object) -> bool:
        return True
