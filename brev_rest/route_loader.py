import os
import sys
import typing
import pathlib
import importlib.util


import astpath  # type: ignore


from . import route


def _get_endpoint_files(path=".") -> typing.Iterable[str]:
    """
    Returns relative paths with use of Route object
    """
    res = astpath.search(path, "//Call/func/*[@id='Router' or @attr='Router']")

    return set(s[0] for s in res)


def _make_package_importable(*, app_path):
    sys_path = pathlib.Path(app_path).parent

    sys.path.append(str(sys_path))


def _load_module_from_file_path(*, app_path, file_path):
    _make_package_importable(app_path=app_path)

    _import_module_in_package(package_path=app_path, module_path=file_path)


def _import_module_in_package(*, package_path, module_path):
    package_path_parent = pathlib.Path(package_path).parent
    module_path = pathlib.Path(module_path).with_suffix("")
    relative_path = os.path.relpath(module_path, package_path_parent)

    python_import_str = relative_path.replace("/", ".")
    __import__(python_import_str)


def _load_endpoint_files(app_path, endpoint_files):
    for ef in endpoint_files:
        _load_module_from_file_path(app_path=app_path, file_path=ef)


def make_routes(*, app_path: str) -> typing.List[route.Router]:
    resolved_path = pathlib.Path(app_path).resolve()

    endpoint_files = _get_endpoint_files(path=resolved_path)

    _load_endpoint_files(app_path, endpoint_files)

    return route.Router.get_all_routes()
