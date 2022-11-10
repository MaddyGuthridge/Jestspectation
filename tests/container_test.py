"""
Tests / List containing test

Tests for whether the ListContaining type
"""
import pytest
from jespectation import (
    DictContainingItems,
    DictContainingKeys,
    DictContainingValues,
    ListContaining,
    SetContaining,
)


@pytest.mark.parametrize(
    ('item', 'matcher'),
    [
        ({1: 'a', 2: 'b', 3: 'c'}, DictContainingKeys({1, 2})),
        ({1: 'a', 2: 'b', 3: 'c'}, DictContainingValues(['a', 'b'])),
        ({1: 'a', 2: 'b', 3: 'c'}, DictContainingItems({1: 'a', 2: 'b'})),
        ([1, 2, 3], ListContaining([1, 2])),
        ({1, 2, 3}, SetContaining({1, 2})),
    ]
)
def test_matches(item, matcher):
    assert item == matcher


@pytest.mark.parametrize(
    ('item', 'matcher'),
    [
        ({1: 'a', 2: 'b', 3: 'c'}, DictContainingKeys({1, 2, 4})),
        ({1: 'a', 2: 'b', 3: 'c'}, DictContainingValues(['a', 'b', 'd'])),
        (
            {1: 'a', 2: 'b', 3: 'c'},
            DictContainingItems({1: 'a', 2: 'b', 3: 'd'}),
        ),
        ([1, 2, 3], ListContaining([1, 2, 4])),
        ({1, 2, 3}, SetContaining({1, 2, 4})),
    ]
)
def test_no_match(item, matcher):
    assert item != matcher
