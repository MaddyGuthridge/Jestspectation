"""
Utility functions
"""


def get_object_type_name(obj: object) -> str:
    return type(obj).__name__


def get_type_name(t: type) -> str:
    return t.__name__
