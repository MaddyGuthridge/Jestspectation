# Jestspectation

Pattern matching helper classes designed to be similar to Jest's expect
matchers, but modified to suit a Pythonic style of programming.

## Basic Usage

```py
import jestspectation as expect
assert {
    "a": 1,
    "b": 2,
    "c": 3,
} == {
    "a": 1,
    "b": expect.Any(int),
    "c": expect.FloatApprox(2.5, magnitude=0.5)
}
```

## Installation

```sh
pip install jestspectation
```

## Usage with Pytest

The library can be used as a pytest plugin, which can give access to much more
detailed error messages when assertions fail.

You can enable it by adding the following lines to your `conftest.py`

```py
pytest_plugins = ("jestspectation.pytest",)
```
