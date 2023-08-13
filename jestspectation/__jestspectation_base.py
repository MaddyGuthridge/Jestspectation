"""
Jestspectation base

Base type used in Jestspectation
"""
from abc import abstractmethod
from .__util import get_object_type_name


REPR_LEN = 25


class JestspectationBase:
    """
    Base class of types used in Jestspectation.
    """
    @abstractmethod
    def get_diff(self, other: object, other_is_lhs: bool) -> list[str]:
        """
        Returns a list of strings showing the difference between this and some
        other object. Each string represents a single line of output.

        This function expects that the two objects have already been checked
        and are not equal.

        Args:
            other (object): object to compare
            other_is_lhs (bool): whether the other object is on the left hand
                side of the expression

        Returns:
            Optional[list[str]]: difference
        """

    def get_contents_repr(self) -> list[str]:
        """
        Returns a list of string representations for the inner contents.

        These strings are considered to be individual tokens, and are used to
        shorten the `__repr__` string of Jestspectation matchers by replacing
        excess items with an ellipsis (...).

        This method should be implemented if the `__repr__` method is not
        overridden.

        Returns:
            list[str]: inner contents
        """
        raise NotImplementedError("Either implement this or override __repr__")

    def get_contents_repr_edges(self) -> tuple[str, str]:
        """
        Returns the opening and closing tokens to surround the contents with.

        This is used to build the representation of Jestspectation matchers
        from a list of contents gathered from the `get_contents_repr` method.

        This method should be implemented if the `__repr__` method is not
        overridden.
        """
        raise NotImplementedError("Either implement this or override __repr__")

    def __repr__(self) -> str:
        contents = self.get_contents_repr()
        open, close = self.get_contents_repr_edges()
        name = get_object_type_name(self)
        str_contents = open

        # Until we've exhausted the contents
        # [a, b, c, ...]
        # Or until we take up all the available chars
        for i, curr in enumerate(contents):
            # If we're about to exceed the max length
            if len(str_contents + curr + ', ...' + close) > REPR_LEN:
                # If this is the last one and it'll still fit
                if (
                    i == len(contents) - 1
                    and len(str_contents + ', ' + curr + close) <= REPR_LEN
                ):
                    str_contents += ', ' + curr
                # Or if it's the first one
                elif i == 0:
                    str_contents += '...'
                # Otherwise, just use the ellipsis
                else:
                    str_contents += ', ...'
                break
            elif str_contents == open:
                str_contents += curr
            else:
                str_contents += ', ' + curr

        str_contents += close

        return f"{name}({str_contents})"
