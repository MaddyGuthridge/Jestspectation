"""
Jestspectation / Pytest

Hooks for Pytest
"""

from typing import Optional

import pytest

from .__config import configure
from .__equals import Equals
from .__jestspectation_base import JestspectationBase


def pytest_assertrepr_compare(
    config: pytest.Config,
    op: str,
    left: object,
    right: object,
) -> Optional[list[str]]:
    """
    Override assert expressions
    """
    if op == "==":
        if isinstance(right, JestspectationBase):
            return right.get_diff(left, True)
        elif isinstance(left, JestspectationBase):
            return left.get_diff(right, False)
        elif configure().pytest_all_diffs:
            return Equals(right).get_diff(left, False)

    return None
