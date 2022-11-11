"""
Jestspectation base

Base type used in Jestspectation
"""
from abc import abstractmethod
from typing import Optional


class JestspectationBase:
    """
    Base class of types used in Jestspectation
    """
    @abstractmethod
    def get_diff(self, other) -> Optional[list[str]]:
        """
        Returns a list of strings showing the difference between this and some
        other object

        Args:
            other (Any): object to compare

        Returns:
            Optional[list[str]]: difference
        """
