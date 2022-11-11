"""
Jestspectation base

Base type used in Jestspectation
"""
from abc import abstractmethod


class JestspectationBase:
    """
    Base class of types used in Jestspectation
    """
    @abstractmethod
    def get_diff(self, other: object) -> list[str]:
        """
        Returns a list of strings showing the difference between this and some
        other object.

        This function expects that the two objects have already been checked
        and are not equal

        Args:
            other (object): object to compare

        Returns:
            Optional[list[str]]: difference
        """
