import pathlib
import typing
import abc
from starlette.types import ASGIApp
import fastapi
import fastapi.utils
import re
import uvicorn
from starlette.routing import get_name

from . import rest
from . import route
from . import startup


class AsgiApp(rest.App):
    @abc.abstractmethod
    def get_server(self) -> ASGIApp:
        raise NotImplementedError()


class BrevFastApiApp(AsgiApp):
    def __init__(
        self,
        *,
        title: str,
        routers: typing.List[route.Router],
        startup_args: rest.AppArgs = None,
        before_app_setup_handler: startup.Handler = startup.nothing_app_handler,
        after_app_setup_handler: startup.Handler = startup.nothing_app_handler,
    ):
        if startup_args is None:
            startup_args = rest.AppArgs(**{"args": (), "kwargs": {}})

        if startup_args["kwargs"].get("title") is None:
            startup_args["kwargs"].pop("title", None)

        self.startup_args = startup_args

        fastapi_kwargs = {"title": title, **startup_args["kwargs"]}

        self.app = fastapi.FastAPI(*startup_args["args"], **fastapi_kwargs)
        before_app_setup_handler(self.app)

        for r in routers:
            self.add_router(r)

        after_app_setup_handler(self.app)

    def add_router(self, router: route.Router) -> None:
        tags = router.kwargs.pop("tags", None)
        explicit_tags = tags if tags is not None else []
        include_router_kwargs = {
            "dependencies": router.kwargs.pop("dependencies", None),
            "responses": router.kwargs.pop("responses", None),
            "default_response_class": router.kwargs.get("default_response_class", None),
        }

        fastapi_api_router = fastapi.APIRouter(**router.kwargs)
        for r in router.routes:
            method = get_name(r.endpoint)

            operation_id = r.kwargs.pop("operation_id", None)
            if operation_id is None:
                operation_id = self.generate_operation_id_for_path(
                    name=router.path, path=r.path, method=method
                )

            fastapi_api_router.add_api_route(
                r.path,
                r.endpoint,
                methods=[method],
                operation_id=operation_id,
                **r.kwargs,
            )

        path = self.make_path(
            suffix=router.path, base=self.startup_args["kwargs"]["api_prefix"]
        )
        self.app.include_router(
            fastapi_api_router,
            prefix=path,
            tags=[router.name, *explicit_tags],
            **include_router_kwargs,
        )

    def make_path(self, *, suffix: str, base: str = ""):
        if base is None or len(base) == 0:
            return suffix
        return f"/{base.strip('/')}/{suffix.lstrip('/')}"

    def generate_operation_id_for_path(
        self, *, name: str, path: str, method: str
    ) -> str:
        """
        Make names like get_xyz, post_xyz_subpath
        TODO: Improve by using variable subpaths and return schema todo things like get_all_endpoints or get_enpoint_by_id
        """
        name = self.clean_name_str(name)
        path = self.clean_name_str(path)
        join = "_" if len(path) > 0 else ""
        operation_id = name + join + path
        operation_id = method.lower() + "_" + operation_id
        return operation_id

    def clean_name_str(self, value: str) -> str:
        value = re.sub("[//{{}}]", "", value)
        value = re.sub("[^0-9a-zA-Z_]", "_", value)
        return value

    def get_server(self) -> ASGIApp:
        return self.app

    def run(self):
        uvicorn.run(self.app)

    def get_meta(self) -> typing.Dict[str, typing.Any]:
        return self.app.openapi()
