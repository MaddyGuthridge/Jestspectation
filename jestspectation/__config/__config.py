"""
Configuration for Jestspectation
"""
from dataclasses import dataclass


@dataclass
class Config:
    """
    Configuration for Jestspectation
    """

    pytest_all_diffs: bool = False
    """
    Whether Jestspectation should provide diffs for all Pytest errors
    """


config = Config()


def configure() -> Config:
    """
    Returns a reference to Jestspectation's configuration, allowing read/write
    access to the options.

    For example:
    ```py
    # Make jestspectation give all diffs for Pytest
    jestspectation.configure().pytest_all_diffs = True
    ```
    """
    return config
