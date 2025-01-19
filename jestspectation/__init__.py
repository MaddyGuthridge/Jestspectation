"""
Jestspectation
==============

Pattern matching helper classes designed to be similar to Jest's expect
matchers, but modified to suit a Pythonic style of programming.
"""

from .__any import Any, Anything
from .__assert import assert_eq
from .__config import configure
from .__containers import (
    DictContainingItems,
    DictContainingKeys,
    DictContainingValues,
    ListContaining,
    ListContainingOnly,
    ListOfLength,
    ObjectContainingItems,
    ObjectContainingProperties,
    SetContaining,
)
from .__equals import Equals, Is
from .__float_approx import FloatApprox
from .__jestspectation_base import JestspectationBase
from .__strings import (
    LinesLike,
    StringContaining,
    StringMatchingRegex,
    TextLike,
)
from .logicals import And, Not, Or, Xor

__all__ = [
    "And",
    "Any",
    "Anything",
    "assert_eq",
    "JestspectationBase",
    "configure",
    "DictContainingKeys",
    "DictContainingValues",
    "DictContainingItems",
    "Equals",
    "FloatApprox",
    "Is",
    "LinesLike",
    "ListContaining",
    "ListContainingOnly",
    "ListOfLength",
    "Not",
    "ObjectContainingProperties",
    "ObjectContainingItems",
    "Or",
    "SetContaining",
    "StringContaining",
    "StringMatchingRegex",
    "TextLike",
    "Xor",
]
