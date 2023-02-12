"""
Diff generators for Python objects
"""
from itertools import zip_longest
from .__util import (
    get_object_type_name,
    sub_diff_delegate,
    diff_wrapper,
)


@diff_wrapper
def diff_list(
    matcher: list,
    other: object,
    other_is_lhs: bool,
) -> list[str]:
    """Difference for Python lists"""
    if not isinstance(other, list):
        return [
            "Type mismatch",
            "Expected list",
            f"Received {get_object_type_name(other)}"
        ]
    ret = []
    # Empty object to check for missing elements
    missing = object()
    # TODO: Find a way to get a nice diff if there are extra objects or
    # something, kinda like Git
    for i, (m, o) in enumerate(zip_longest(matcher, other, fillvalue=missing)):
        if m is missing:
            # this element is missing from the matcher
            ret += [f'++ [{i}] {repr(o)}']
        elif o is missing:
            # this element is missing from the other
            ret += [f'-- [{i}] {repr(m)}']
        else:
            sub_diff = sub_diff_delegate(m, o, other_is_lhs)
            if sub_diff is not None:
                # Add a dot point to the first one to make it pretty
                sub_diff[0] = f'!! [{i}] ' + sub_diff[0][3:]
                ret += sub_diff

    return ret


@diff_wrapper
def diff_set(
    matcher: set,
    other: object,
    other_is_lhs: bool,
) -> list[str]:
    """Difference for Python sets"""
    if not isinstance(other, set):
        return [
            "Type mismatch",
            "Expected set",
            f"Received {get_object_type_name(other)}"
        ]
    ret = []
    # Missing
    for e in matcher:
        if e not in other:
            ret += [f"-- {repr(e)}"]

    # Additional
    for e in other:
        if e not in matcher:
            ret += [f"++ {repr(e)}"]

    return ret


@diff_wrapper
def diff_dict(
    matcher: dict,
    other: object,
    other_is_lhs: bool,
) -> list[str]:
    """Difference for Python dicts"""
    if not isinstance(other, dict):
        return [
            "Type mismatch",
            "Expected dict",
            f"Received {get_object_type_name(other)}"
        ]

    def diff_str(key, d: dict) -> str:
        return f"{repr(key)}: {repr(d[key])}"

    ret = []
    # Missing
    for e in matcher.keys():
        if e not in other.keys():
            ret += [f"-- {diff_str(e, matcher)}"]

    # Additional
    for e in other.keys():
        if e not in matcher.keys():
            ret += [f"++ {diff_str(e, other)}"]

    # Non-equal keys
    for e in matcher.keys():
        if e in other.keys():
            sub_diff = sub_diff_delegate(matcher[e], other[e], other_is_lhs)
            if sub_diff is not None:
                ret += [
                    f"!! {diff_str(e, matcher)} == {diff_str(e, other)}"
                ] + sub_diff

    return ret
