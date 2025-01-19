"""
Tests for logical combinators
"""

import pytest

from jestspectation import And, Any, Or, Xor


@pytest.mark.parametrize("matcher_type", [And, Or, Xor])
def test_too_few_enough_matchers(matcher_type):
    with pytest.raises(TypeError):
        # Requires at least two matchers
        matcher_type(Any(int))
