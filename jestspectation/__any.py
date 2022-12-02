"""
Matchers that match close to anything
"""
from .__jestspectation_base import JestspectationBase
from .__util import get_type_name, get_object_type_name, safe_diff_wrapper


class Any(JestspectationBase):
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
        return f"Any({get_type_name(self.__match_type)})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__match_type)

    @safe_diff_wrapper
    def get_diff(self, other: object, other_is_lhs: bool) -> list[str]:
        return [
            'Type mismatch',
            f'Expected any object of type {get_type_name(self.__match_type)}',
            f'Received {repr(other)} ({get_object_type_name(other)})',
        ]


class Anything(JestspectationBase):
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

    def get_diff(self, other: object, other_is_lhs: bool) -> list[str]:
        raise Exception(f"Anything() should have matched {other}")
