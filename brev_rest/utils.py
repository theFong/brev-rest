import sys


def clear_modules(path):
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