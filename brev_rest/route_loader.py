import typing
import pathlib
import importlib.util


import astpath  # type: ignore


from . import route


def _get_endpoint_files(path=".") -> typing.Iterable[str]:
    """
    Returns relative paths with use of Route object
    """
    res = astpath.search(path, "//Call/func/*[@id='Route' or @attr='Route']")

    return set(s[0] for s in res)


def _load_module_from_file_path(path):
    name = pathlib.Path(path).stem
    spec = importlib.util.spec_from_file_location(f"brev_endpoint_{name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)


def _load_endpoint_files(app_path, endpoint_files):
    for ef in endpoint_files:
        _load_module_from_file_path(ef)


def make_routes(*, app_path: str) -> typing.List[route.Route]:
    resolved_path = pathlib.Path(app_path).resolve()

    endpoint_files = _get_endpoint_files(path=resolved_path)

    _load_endpoint_files(app_path, endpoint_files)

    return route.all_routes
