"""
Jestspectation / Pytest

Hooks for Pytest
"""
import pytest
from .__jestspectation_base import JestspectationBase


def pytest_assertrepr_compare(
    config: pytest.Config,
    op: str,
    left: object,
    right: object,
):
    """
    Override assert expressions
    """
    if op == "==":
        expr = f"{repr(left)} == {repr(right)}"
        if isinstance(right, JestspectationBase):
            return right.get_diff(left, expr)
        if isinstance(left, JestspectationBase):
            return left.get_diff(right, expr)
    return None
