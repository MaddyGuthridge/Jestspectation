"""
Utility functions
"""
from functools import wraps
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
    diff_function: Callable[[T, object, bool], list[str]],
) -> Callable[[T, object, bool], Optional[list[str]]]:
    """
    Decorator around diff functions to add an equality statement. Also returns
    None if values are equal
    """
    @wraps(diff_function)
    def wrapper(
        matcher: T,
        other: object,
        other_is_lhs: bool,
    ) -> Optional[list[str]]:
        if matcher == other:
            return None
        if other_is_lhs:
            eq_expr = f"{repr(other)} == {repr(matcher)}"
        else:
            eq_expr = f"{repr(matcher)} == {repr(other)}"
        return [eq_expr] + diff_function(matcher, other, other_is_lhs)
    return wrapper


def safe_diff_wrapper(
    diff_function: Callable[[T, object, bool], list[str]],
) -> Callable[[T, object, bool], list[str]]:
    """
    Decorator around diff functions to add an equality statement if they are
    not equal to reduce repetition
    """
    @wraps(diff_function)
    def wrapper(matcher: T, other: object, other_is_lhs: bool) -> list[str]:
        if other_is_lhs:
            eq_expr = f"{repr(other)} == {repr(matcher)}"
        else:
            eq_expr = f"{repr(matcher)} == {repr(other)}"
        return [eq_expr] + diff_function(matcher, other, other_is_lhs)
    return wrapper


def sub_diff_delegate(
    matcher: object,
    other: object,
    other_is_lhs: bool,
    indent: bool = True,
) -> Optional[list[str]]:
    """
    Calculate and return a sub-diff

    This is used to recursively calculate the difference between two objects,
    including Python built-ins
    """
    # Avoid a circular import
    from . import __py_diffs as py_diffs

    def do_sub_diff(
        matcher: object,
        other: object,
        other_is_lhs: bool,
    ) -> Optional[list[str]]:
        """
        Inner function so we can wrap up the return values
        """
        from .__jestspectation_base import JestspectationBase
        if matcher == other:
            return None
        # Handle out types
        if isinstance(matcher, JestspectationBase):
            return matcher.get_diff(other, other_is_lhs)

        elif isinstance(matcher, list):
            return py_diffs.diff_list(matcher, other, other_is_lhs)

        elif isinstance(matcher, set):
            return py_diffs.diff_set(matcher, other, other_is_lhs)

        elif isinstance(matcher, dict):
            return py_diffs.diff_dict(matcher, other, other_is_lhs)

        # For other objects, just do the repr
        if matcher == other:
            return None
        else:
            if other_is_lhs:
                eq_expr = f"{repr(other)} == {repr(matcher)}"
            else:
                eq_expr = f"{repr(matcher)} == {repr(other)}"
            return [
                eq_expr,
                "Value mismatch",
                f"Expected {repr(matcher)}",
                f"Received {repr(other)}",
            ]

    diff = do_sub_diff(matcher, other, other_is_lhs)
    if diff is None:
        return None
    if indent:
        return indent_lines(diff, 3)
    else:
        return diff
