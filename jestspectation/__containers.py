from abc import abstractmethod
from collections.abc import Iterable
from typing import Optional, TypeGuard
from .__jestspectation_base import JestspectationBase


class JestspectationContainer(JestspectationBase):
    """
    Base type for container matchers
    """

    @staticmethod
    @abstractmethod
    def _get_allowed_types() -> tuple[type, ...]:
        """
        Returns the allowed match types of the container
        """

    def __is_allowed_type(self, other) -> TypeGuard[Iterable]:
        """
        Returns whether other is an allowed type
        """
        return isinstance(other, self._get_allowed_types())

    @abstractmethod
    def _match_inner_callback(self, item: object, other: Iterable) -> bool:
        """
        Returns whether item matches an entry in the container.

        Defined by subclasses to get the array of missing properties
        """

    @abstractmethod
    def _get_items(self) -> Iterable:
        """
        Returns the Iterable of items that should be in the container
        """

    def __get_misses(self, other: Iterable) -> list:
        return list(map(
            lambda i: i[1],
            filter(
                lambda i: i[0] is False,
                (
                    (self._match_inner_callback(i, other), i)
                    for i in self._get_items()
                )
            )
        ))

    def get_diff(self, other: object) -> Optional[list[str]]:
        if self == other:
            return None
        if not self.__is_allowed_type(other):
            return [
                f"Expected {self}, but received a {type(other).__name__}"
            ]
        misses = self.__get_misses(other)
        return [
            f"Expected {repr(other)} to be {self}, but was missing",
        ] + [f"   {repr(i)}" for i in misses]

    def __eq__(self, other: object) -> bool:
        if not self.__is_allowed_type(other):
            return False
        return len(self.__get_misses(other)) == 0


class ListContaining(JestspectationContainer):
    """
    Matches any list containing all the given items
    """

    def __init__(self, items: list) -> None:
        """
        Matches any list containing all the given items

        Args:
            items (list): items to check for
        """
        self.__items = items

    def __repr__(self) -> str:
        return f"ListContaining({repr(self.__items)})"

    @staticmethod
    def _get_allowed_types() -> tuple[type, ...]:
        return (list,)

    def _get_items(self) -> Iterable:
        return self.__items

    def _match_inner_callback(self, item: object, other: Iterable) -> bool:
        return item in other


class SetContaining(JestspectationContainer):
    """
    Matches any set containing all the given items
    """

    def __init__(self, items: set) -> None:
        """
        Matches any set containing all the given items

        Args:
            items (set): items to check for
        """
        self.__items = items

    def __repr__(self) -> str:
        return f"SetContaining({repr(self.__items)})"

    @staticmethod
    def _get_allowed_types() -> tuple[type, ...]:
        return (set,)

    def _get_items(self) -> Iterable:
        return self.__items

    def _match_inner_callback(self, item: object, other: Iterable) -> bool:
        return item in other


class DictContainingKeys(JestspectationContainer):
    """
    Matches any dictionary containing all the given keys
    """

    def __init__(self, keys: set) -> None:
        """
        Matches any dictionary containing all the given keys

        Args:
            keys (set): set of keys to match
        """
        self.__keys = keys

    def __repr__(self) -> str:
        return f"DictContainingKeys({repr(self.__keys)})"

    @staticmethod
    def _get_allowed_types() -> tuple[type, ...]:
        return (dict,)

    def _get_items(self) -> Iterable:
        return self.__keys

    def _match_inner_callback(self, item: object, other: Iterable) -> bool:
        return item in other


class DictContainingValues(JestspectationContainer):
    """
    Matches any dictionary containing all the given values
    """

    def __init__(self, values: list) -> None:
        """
        Matches any dictionary containing all the given values

        Args:
            values (list): list of values to match
        """
        self.__values = values

    def __repr__(self) -> str:
        return f"DictContainingValues({repr(self.__values)})"

    @staticmethod
    def _get_allowed_types() -> tuple[type, ...]:
        return (dict,)

    def _get_items(self) -> Iterable:
        return self.__values

    def _match_inner_callback(self, item: object, other: Iterable) -> bool:
        # TODO: Fix type safety
        return item in other.values()  # type: ignore


class DictContainingItems(JestspectationContainer):
    """
    Matches any dictionary containing all the given items, where an item is a
    key-value pair.
    """

    def __init__(self, items: dict) -> None:
        """
        Matches any dictionary containing all the given items, where an item is
        a key-value pair.

        Args:
            items (dict): dict of items to match
        """
        self.__items = items

    def __repr__(self) -> str:
        return f"DictContainingItems({repr(self.__items)})"

    @staticmethod
    def _get_allowed_types() -> tuple[type, ...]:
        return (dict,)

    def _get_items(self) -> Iterable:
        return self.__items.items()

    def _match_inner_callback(self, item: object, other: Iterable) -> bool:
        # TODO: Use generics to make this type-safe
        return item[0] in other and other[item[0]] == item[1]  # type: ignore
