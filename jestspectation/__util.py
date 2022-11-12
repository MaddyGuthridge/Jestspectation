"""
Utility functions
"""
from typing import Optional, Callable, TypeVar

T = TypeVar('T')


def get_object_type_name(obj: object) -> str:
    """
    Return the name of the type of an object
    """
    return type(obj).__name__


def get_type_name(t: type) -> str:
    """
    Return the name of a type
    """
    return t.__name__


def indent_lines(lines: list[str], amount: int) -> list[str]:
    """
    Return a list of strings indented by the given amount
    """
    return list(map(
        lambda line: f"{' ' * amount}{line}",
        lines,
    ))


def diff_wrapper(
    diff_function: Callable[[T, object], list[str]],
) -> Callable[[T, object], Optional[list[str]]]:
    """
    Decorator around diff functions to add an equality statement. Also returns
    None if values are equal
    """
    def wrapper(matcher: T, other: object) -> Optional[list[str]]:
        if matcher == other:
            return None
        return [
            f"{repr(matcher)} == {repr(other)}",
        ] + diff_function(matcher, other)
    return wrapper


def safe_diff_wrapper(
    diff_function: Callable[[T, object], list[str]],
) -> Callable[[T, object], list[str]]:
    """
    Decorator around diff functions to add an equality statement if they are
    not equal to reduce repetition
    """
    def wrapper(matcher: T, other: object) -> list[str]:
        return [
            f"{repr(matcher)} == {repr(other)}",
        ] + diff_function(matcher, other)
    return wrapper


def sub_diff_delegate(
    matcher: object,
    other: object,
    indent: bool = True,
) -> Optional[list[str]]:
    """
    Calculate and return a sub-diff

    This is used to recursively calculate the difference between two objects,
    including Python built-ins
    """
    # Avoid a circular import
    from . import __py_diffs as py_diffs

    def do_sub_diff(matcher: object, other: object) -> Optional[list[str]]:
        """
        Inner function so we can wrap up the return values
        """
        from .__jestspectation_base import JestspectationBase
        if matcher == other:
            return None
        # Handle out types
        if isinstance(matcher, JestspectationBase):
            return matcher.get_diff(other)

        elif isinstance(matcher, list):
            return py_diffs.diff_list(matcher, other)

        elif isinstance(matcher, set):
            return py_diffs.diff_set(matcher, other)

        elif isinstance(matcher, dict):
            return py_diffs.diff_dict(matcher, other)

        # For other objects, just do the repr
        if matcher == other:
            return None
        else:
            return [
                f"{repr(matcher)} == {repr(other)}",
                "Value mismatch",
                f"Expected {repr(matcher)}",
                f"Received {repr(other)}",
            ]

    diff = do_sub_diff(matcher, other)
    if diff is None:
        return None
    if indent:
        return indent_lines(diff, 3)
    else:
        return diff
