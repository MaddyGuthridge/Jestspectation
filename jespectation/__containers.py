

class ListContaining:
    def __init__(self, items: list) -> None:
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
    def __init__(self, items: set) -> None:
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
    def __init__(self, keys: set) -> None:
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
    def __init__(self, values: list) -> None:
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
    def __init__(self, items: dict) -> None:
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
