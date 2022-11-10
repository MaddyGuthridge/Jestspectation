

class ListContaining:
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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, list):
            return False
        return all(
            i in other
            for i in self.__items
        )


class SetContaining:
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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, set):
            return False
        return all(
            i in other
            for i in self.__items
        )


class DictContainingKeys:
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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, dict):
            return False
        return all(
            i in other.keys()
            for i in self.__keys
        )


class DictContainingValues:
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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, dict):
            return False
        return all(
            i in other.values()
            for i in self.__values
        )


class DictContainingItems:
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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, dict):
            return False
        return all(
            other[k] == v
            for k, v in self.__items.items()
        )
