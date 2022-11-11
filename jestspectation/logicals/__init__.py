"""
Logicals

Matchers that can be used to perform logical operations on other matchers
"""

from .__and import And
from .__not import Not
from .__or import Or
from .__xor import Xor


__all__ = [
    'And',
    'Not',
    'Or',
    'Xor',
]
