import sys
import typing


def clear_modules(path: str):
    """
    Removing discoverability and reference to packages
    """
    to_remove_keys = []
    for k, v in sys.modules.items():
        if hasattr(v, "__file__") and v.__file__ is not None and path in v.__file__:
            to_remove_keys.append(k)
    for k in to_remove_keys:
        sys.modules.pop(k)

    sys.path = [p for p in sys.path if path not in p]


def merge_null_dict(
    d1: typing.Dict[typing.Any, typing.Any], d2: typing.Dict[typing.Any, typing.Any]
):
    """
    Merge to dicts and take non-None value
     if either value does not exist add
     if one or the other is not none take non none value
     if both non none take d2
    """

    new = dict(d1)

    for k, v in d2.items():
        if v is not None:
            new[k] = v
        else:
            if new.get(k) is None:
                new[k] = v

    return new
