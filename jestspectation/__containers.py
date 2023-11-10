"""
Matchers for specific container types
"""

from abc import abstractmethod
from collections.abc import Iterable, ItemsView
from typing import Any, TypeVar, Generic, cast
from typing_extensions import TypeGuard
from .__jestspectation_base import JestspectationBase
from .__util import get_object_type_name, safe_diff_wrapper, sub_diff_delegate


T = TypeVar('T', bound=Iterable)


class JestspectationContainer(JestspectationBase, Generic[T]):
    """
    Base type for container matchers
    """

    @staticmethod
    @abstractmethod
    def _get_allowed_types() -> tuple[type, ...]:
        """
        Returns the allowed match types of the container
        """

    def __is_allowed_type(self, other) -> TypeGuard[T]:
        """
        Returns whether other is an allowed type
        """
        return isinstance(other, self._get_allowed_types())

    @abstractmethod
    def _is_present(self, item: object, other: T) -> bool:
        """
        Returns whether item matches an entry in the container.

        Defined by subclasses to calculate the array of missing properties.
        """

    def _is_correct(self, item: object, other: T) -> bool:
        """
        Returns whether an item is correct, given that it is present

        If this is called, the item is already guaranteed to be present.

        By default, this assumes that all present items are correct.
        """
        return True

    def _format_sub_diff(
        self,
        item: object,
        other: T,
        other_is_lhs: bool,
    ) -> list[str]:
        """
        Returns the sub-diff for the given item compared to its actual value.
        """
        raise NotImplementedError(
            "This should be implemented for all containers that can have "
            "present but incorrect items"
        )

    def _format_missing_item(
        self,
        item: object,
    ) -> str:
        """
        Returns a string representing the missing item. By default this is just
        the repr.
        """
        return repr(item)

    @abstractmethod
    def _get_items(self) -> T:
        """
        Returns the Iterable of items that should be in the container
        """

    def __get_misses(self, other: T) -> list:
        """Filter the list of items to only include the missing ones"""
        return list(map(
            lambda i: i[1],
            filter(
                lambda i: i[0] is False,
                (
                    (self._is_present(i, other), i)
                    for i in self._get_items()
                )
            )
        ))

    def __get_incorrect(self, other: T) -> list:
        """
        Filter the list of items to only include the present but incorrect ones
        """
        return list(map(
            lambda i: i[1],
            filter(
                lambda i: i[0] is True,
                (
                    (
                        # Item is present, but not correct
                        self._is_present(i, other)
                        and not self._is_correct(i, other),
                        i
                    )
                    for i in self._get_items()
                )
            )
        ))

    @safe_diff_wrapper
    def get_diff(self, other: object, other_is_lhs: bool) -> list[str]:
        if not self.__is_allowed_type(other):
            return [
                "Type mismatch",
                f"Expected {self}",
                f"Received object of type {get_object_type_name(other)}"
            ]
        misses = self.__get_misses(other)
        incorrect = self.__get_incorrect(other)
        if len(misses) > 0 and len(incorrect) > 0:
            ret = ["Missing and incorrect properties"]
        elif len(misses) > 0:
            ret = ["Missing properties"]
        else:
            # len(incorrect) > 0
            ret = ["Incorrect properties"]
        ret += [f"Expected a {repr(self)}"]

        if len(misses) != 0:
            ret += [f"-- {self._format_missing_item(i)}" for i in misses]

        if len(incorrect) != 0:
            for i in incorrect:
                sub_diff = self._format_sub_diff(i, other, other_is_lhs)
                assert sub_diff is not None
                # Add a dot point to the first one to make it pretty
                sub_diff[0] = '!! ' + sub_diff[0][3:]
                ret += sub_diff

        return ret

    def __eq__(self, other: object) -> bool:
        if not self.__is_allowed_type(other):
            return False
        return (
            len(self.__get_misses(other)) == 0
            and len(self.__get_incorrect(other)) == 0
        )


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

    def get_contents_repr(self) -> list[str]:
        return [repr(v) for v in self.__items]

    def get_contents_repr_edges(self) -> tuple[str, str]:
        return '[', ']'

    @staticmethod
    def _get_allowed_types() -> tuple[type, ...]:
        return (list,)

    def _get_items(self) -> list:
        return self.__items

    def _is_present(self, item: object, other: list) -> bool:
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

    def get_contents_repr(self) -> list[str]:
        return [repr(v) for v in self.__items]

    def get_contents_repr_edges(self) -> tuple[str, str]:
        return '{', '}'

    @staticmethod
    def _get_allowed_types() -> tuple[type, ...]:
        return (set,)

    def _get_items(self) -> set:
        return self.__items

    def _is_present(self, item: object, other: set) -> bool:
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

    def get_contents_repr(self) -> list[str]:
        return [repr(v) for v in self.__keys]

    def get_contents_repr_edges(self) -> tuple[str, str]:
        return '{', '}'

    @staticmethod
    def _get_allowed_types() -> tuple[type, ...]:
        return (dict,)

    def _get_items(self) -> set:
        return self.__keys

    def _is_present(self, item: object, other: set) -> bool:
        return item in other


class ObjectContainingProperties(JestspectationContainer):
    """
    Matches any object containing all the given properties. Note that this does
    not check property values - just the presence of those properties.
    """

    def __init__(self, properties: set[str]) -> None:
        """
        Matches any object containing all the given properties. Note that this
        does not check property values - just the presence of those properties.

        Args:
            properties (set): set of properties to match
        """
        self.__properties = properties

    def get_contents_repr(self) -> list[str]:
        return sorted(self.__properties)

    def get_contents_repr_edges(self) -> tuple[str, str]:
        return '', ''

    @staticmethod
    def _get_allowed_types() -> tuple[type, ...]:
        return (object,)

    def _get_items(self) -> list[str]:
        return sorted(self.__properties)

    def _is_present(self, item: object, other: set) -> bool:
        return item in dir(other)

    def _format_missing_item(self, item: object) -> str:
        return cast(str, item)


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

    def get_contents_repr(self) -> list[str]:
        return [repr(v) for v in self.__values]

    def get_contents_repr_edges(self) -> tuple[str, str]:
        return '[', ']'

    @staticmethod
    def _get_allowed_types() -> tuple[type, ...]:
        return (dict,)

    def _get_items(self) -> list:
        return self.__values

    def _is_present(self, item: object, other: list) -> bool:
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

    def get_contents_repr(self) -> list[str]:
        return [f"{repr(i[0])}: {repr(i[1])}" for i in self.__items.items()]

    def get_contents_repr_edges(self) -> tuple[str, str]:
        return '{', '}'

    @staticmethod
    def _get_allowed_types() -> tuple[type, ...]:
        return (dict,)

    def _get_items(self) -> ItemsView:
        return self.__items.items()

    def _is_present(self, item: object, other: ItemsView) -> bool:
        # TODO: Use generics to make this type-safe
        return item[0] in other  # type: ignore

    def _is_correct(self, item: object, other: ItemsView) -> bool:
        return other[item[0]] == item[1]  # type: ignore

    def _format_sub_diff(
        self,
        item: object,
        other: ItemsView,
        other_is_lhs: bool,
    ) -> list[str]:
        # Lots of type: ignores here because I can't figure out how to make
        # this type-safe :(
        # Just need to get good test coverage
        diff = sub_diff_delegate(
            item[1],  # type: ignore
            other[item[0]],  # type: ignore
            other_is_lhs,
        )
        assert diff is not None
        self_repr = self._format_missing_item(item)
        other_repr = f"{repr(item[0])}: {repr(other[item[0]])}"  # type: ignore
        if other_is_lhs:
            eq_expr = f"   {other_repr} == {self_repr}"
        else:
            eq_expr = f"   {self_repr} == {other_repr}"
        return [eq_expr] + diff

    def _format_missing_item(self, item: object) -> str:
        # Format like dict keys
        return f"{repr(item[0])}: {repr(item[1])}"  # type: ignore


class ObjectContainingItems(JestspectationContainer):
    """
    Matches any object containing all the given items, where an item is a
    property-value pair.
    """

    def __init__(self, items: dict[str, Any]) -> None:
        """
        Matches any object containing all the given items, where an item is a
        property-value pair.

        Args:
            items (dict): dict of items to match
        """
        self.__items = items

    def __repr__(self) -> str:
        inners = []
        for property, value in self.__items.items():
            inners.append(f"{property} = {value}")

        return f"ObjectContainingItems({', '.join(inners)})"

    def get_contents_repr(self) -> list[str]:
        return [f"{repr(i[0])} == {repr(i[1])}" for i in self.__items.items()]

    def get_contents_repr_edges(self) -> tuple[str, str]:
        return '', ''

    @staticmethod
    def _get_allowed_types() -> tuple[type, ...]:
        return (object,)

    def _get_items(self) -> ItemsView:
        return self.__items.items()

    def _is_present(self, item: object, other: object) -> bool:
        # TODO: Use generics to make this type-safe
        return item[0] in dir(other)  # type: ignore

    def _is_correct(self, item: object, other: object) -> bool:
        return getattr(other, item[0]) == item[1]  # type: ignore

    def _format_sub_diff(
        self,
        item: object,
        other: ItemsView,
        other_is_lhs: bool,
    ) -> list[str]:
        # Lots of type: ignores here because I can't figure out how to make
        # this type-safe :(
        # Just need to get good test coverage
        other_value = getattr(other, item[0])  # type: ignore
        diff = sub_diff_delegate(
            item[1],  # type: ignore
            other_value,
            other_is_lhs,
        )
        assert diff is not None
        self_repr = self._format_missing_item(item)
        other_repr = f"{item[0]} = {repr(other_value)}"  # type: ignore
        if other_is_lhs:
            eq_expr = f"   {other_repr} == {self_repr}"
        else:
            eq_expr = f"   {self_repr} == {other_repr}"
        return [eq_expr] + diff

    def _format_missing_item(self, item: object) -> str:
        # Format like dict keys
        return f"{item[0]} = {repr(item[1])}"  # type: ignore


class ListOfLength(JestspectationBase):
    """
    Matches any list of the given length
    """

    def __init__(self, length: int) -> None:
        """
        Matches any list of a given length

        Args:
            length (int): the expected length of the list

        Raises:
            ValueError: length is < 0
        """
        if length < 0:
            raise ValueError("List length cannot be < 0")
        self.__length = length

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, list):
            return False
        return len(other) == self.__length

    def __repr__(self) -> str:
        return f"ListOfLength({self.__length})"

    def get_diff(self, other: object, other_is_lhs: bool) -> list[str]:
        if not isinstance(other, list):
            return [
                "Type mismatch",
                f"Expected object of type list ({repr(self)})",
                f"Received object of type {type(other).__name__} ({other})",
            ]

        return [
            "Length failed to match",
            f"Expected list of length {self.__length}",
            f"Received list of length {len(other)} ({other})",
        ]
