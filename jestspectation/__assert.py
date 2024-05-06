"""
Helper functions for making assertions with pretty error messages.
"""
from typing import TypeVar
from jestspectation import Equals


T = TypeVar('T')


def assert_eq(lhs: T, rhs: T) -> None:
    """
    Asserts that `lhs` is equal to `rhs`

    ## Args

    * `lhs`: left-hand side of expression
    * `rhs`: right-hand side of expression

    ## Raises

    * `AssertionError`: when `lhs != rhs`
    """
    wrapped = Equals(lhs)

    if wrapped != rhs:
        diff = '\n'.join(wrapped.get_diff(rhs, False))
        raise AssertionError(diff)
