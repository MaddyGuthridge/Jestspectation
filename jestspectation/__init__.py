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
    ListOfLength,
)
from .__float_approx import FloatApprox
from .__equals import Equals, Is
from .logicals import And, Not, Or, Xor
from .__strings import (
    StringMatchingRegex,
    StringContaining,
    TextLike,
    LinesLike,
)
from .__config import configure


__all__ = [
    'And',
    'Any',
    'Anything',
    'configure',
    'DictContainingKeys',
    'DictContainingValues',
    'DictContainingItems',
    'Equals',
    'FloatApprox',
    'Is',
    'LinesLike',
    'ListContaining',
    'ListOfLength',
    'Not',
    'Or',
    'SetContaining',
    'StringContaining',
    'StringMatchingRegex',
    'TextLike',
    'Xor',
]
