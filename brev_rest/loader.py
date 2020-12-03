import os
import sys
import typing
import pathlib
import logging
import astpath


from . import route
from . import startup

logger = logging.getLogger("brev-rest")


def _get_endpoint_files(
    path: typing.Union[str, pathlib.Path] = "."
) -> typing.Iterable[str]:
    """
    Returns relative paths with use of Route object
    """
    logger.debug("finding router files")
    res = astpath.search(path, ".//Call/func/*[@id='Router' or @attr='Router']")

    return set(s[0] for s in res)


def _make_package_importable(*, app_path: str):
    logger.debug(f"making importable: {app_path}")
    sys_path = pathlib.Path(app_path).parent
    sys_path_str = str(sys_path)

    if sys_path_str not in sys.path:
        sys.path.append(sys_path_str)


def _load_module_from_file_path(*, app_path: str, file_path: str):
    logger.debug(f"loading module: {app_path}")
    _make_package_importable(app_path=app_path)

    _import_module_in_package(package_path=app_path, module_path=file_path)


def _import_module_in_package(*, package_path: str, module_path: str):
    logger.debug(f"importing module: {module_path} in package: {package_path}")
    package_path_parent = pathlib.Path(package_path).parent
    module_path_ = pathlib.Path(module_path).with_suffix("")
    relative_path = os.path.relpath(module_path_, package_path_parent)

    python_import_str = relative_path.replace("/", ".")

    if python_import_str.endswith("__init__"):
        python_import_str = python_import_str.rstrip(".__init__")

    __import__(python_import_str)


def _load_files_in_package(*, root_path: str, file_paths: typing.Iterable[str]):
    logger.debug("loading all files in package")
    for fp in file_paths:
        _load_module_from_file_path(app_path=root_path, file_path=fp)


def init_setup(*, app_path: str):
    logger.info("doing init setup")
    resolved_path = pathlib.Path(app_path).resolve()

    setup_files = _get_setup_files(path=resolved_path)
    logger.debug(f"found setup files: {list(setup_files)}")

    _load_files_in_package(root_path=app_path, file_paths=setup_files)

    startup.Setup.did_setup()
    logger.info("done setting up")


def _get_setup_files(*, path: typing.Union[str, pathlib.Path]):
    """
    Returns relative paths with use of Startup object
    """
    logger.info("finding setup files")
    res = astpath.search(path, ".//Call/func/*[@id='Setup' or @attr='Setup']")

    return set(s[0] for s in res)


def make_routers(*, app_path: str) -> typing.List[route.Router]:
    logger.info(f"making routers {app_path}")
    resolved_path = pathlib.Path(app_path).resolve()

    endpoint_files = _get_endpoint_files(path=resolved_path)
    logger.debug(f"endpoint files: {list(endpoint_files)}")

    _load_files_in_package(root_path=app_path, file_paths=endpoint_files)

    auto_loaded_routers = route.Router.get_all_routers()

    manual_routers = startup.Setup.get_routers_to_add()

    routers = manual_routers + [
        r for r in auto_loaded_routers if r not in manual_routers
    ]
    logger.info("done making routers")
    return routers
