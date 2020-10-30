import os
import sys
import typing
import pathlib


import astpath  # type: ignore


from . import route
from . import startup


def _get_endpoint_files(path=".") -> typing.Iterable[str]:
    """
    Returns relative paths with use of Route object
    """
    res = astpath.search(path, "//Call/func/*[@id='Router' or @attr='Router']")

    return set(s[0] for s in res)


def _make_package_importable(*, app_path):
    sys_path = pathlib.Path(app_path).parent
    sys_path_str = str(sys_path)

    if sys_path_str not in sys.path:
        sys.path.append(sys_path_str)


def _load_module_from_file_path(*, app_path, file_path):
    _make_package_importable(app_path=app_path)

    _import_module_in_package(package_path=app_path, module_path=file_path)


def _import_module_in_package(*, package_path, module_path):
    package_path_parent = pathlib.Path(package_path).parent
    module_path = pathlib.Path(module_path).with_suffix("")
    relative_path = os.path.relpath(module_path, package_path_parent)

    python_import_str = relative_path.replace("/", ".")

    if python_import_str.endswith("__init__"):
        python_import_str = python_import_str.rstrip(".__init__")

    __import__(python_import_str)


def _load_files_in_package(*, root_path, file_paths):
    for fp in file_paths:
        _load_module_from_file_path(app_path=root_path, file_path=fp)


def init_setup(*, app_path: str):
    resolved_path = pathlib.Path(app_path).resolve()

    setup_files = _get_setup_files(path=resolved_path)

    _load_files_in_package(root_path=app_path, file_paths=setup_files)

    startup.Setup.did_setup()


def _get_setup_files(*, path):
    """
    Returns relative paths with use of Startup object
    """
    res = astpath.search(path, "//Call/func/*[@id='Setup' or @attr='Setup']")

    return set(s[0] for s in res)


def make_routers(*, app_path: str) -> typing.List[route.Router]:
    resolved_path = pathlib.Path(app_path).resolve()

    endpoint_files = _get_endpoint_files(path=resolved_path)

    _load_files_in_package(root_path=app_path, file_paths=endpoint_files)

    auto_loaded_routers = route.Router.get_all_routers()

    manual_routers = startup.Setup.get_routers_to_add()

    return manual_routers + [r for r in auto_loaded_routers if r not in manual_routers]
