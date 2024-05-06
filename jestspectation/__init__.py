"""
Jestspectation
==============

Pattern matching helper classes designed to be similar to Jest's expect
matchers, but modified to suit a Pythonic style of programming.
"""

from .__jestspectation_base import JestspectationBase
from .__any import Any, Anything
from .__containers import (
    DictContainingKeys,
    DictContainingValues,
    DictContainingItems,
    ListContaining,
    ListContainingOnly,
    ListOfLength,
    SetContaining,
    ObjectContainingProperties,
    ObjectContainingItems,
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
from .__assert import assert_eq
from .__config import configure


__all__ = [
    'And',
    'Any',
    'Anything',
    'assert_eq',
    'JestspectationBase',
    'configure',
    'DictContainingKeys',
    'DictContainingValues',
    'DictContainingItems',
    'Equals',
    'FloatApprox',
    'Is',
    'LinesLike',
    'ListContaining',
    'ListContainingOnly',
    'ListOfLength',
    'Not',
    'ObjectContainingProperties',
    'ObjectContainingItems',
    'Or',
    'SetContaining',
    'StringContaining',
    'StringMatchingRegex',
    'TextLike',
    'Xor',
]
