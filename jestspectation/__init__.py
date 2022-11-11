"""
Jestspectation
==============

Pattern matching helper classes designed to be similar to Jest's expect
matchers, but modified to suit a Pythonic style of programming.
"""

from .__any import Any, Anything
from .__containers import (
    DictContainingKeys,
    DictContainingValues,
    DictContainingItems,
    ListContaining,
    SetContaining,
)
from .__float_approx import FloatApprox
from .__equals import Is
from .__logicals import And, Not, Or, Xor
from .__str_match import StringMatchingRegex


__all__ = [
    'And',
    'Any',
    'Anything',
    'DictContainingKeys',
    'DictContainingValues',
    'DictContainingItems',
    'FloatApprox',
    'Is',
    'ListContaining',
    'Not',
    'Or',
    'SetContaining',
    'StringMatchingRegex',
    'Xor',
]
