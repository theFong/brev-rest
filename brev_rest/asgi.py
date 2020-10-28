import typing
import abc
from starlette.types import ASGIApp
import fastapi
import fastapi.utils
import re
import uvicorn  # type: ignore
from starlette.routing import get_name

from . import rest
from . import route as brev_route


class Asgi(rest.App):
    @abc.abstractmethod
    def get_server(self) -> ASGIApp:
        raise NotImplementedError()


class BrevFastApi(Asgi):
    def __init__(self, title, routers: typing.List[brev_route.Router]):
        self.app = fastapi.FastAPI(title=title)

        for r in routers:
            self.add_router(r)

    def add_router(self, router: brev_route.Router):
        fastapi_api_router = fastapi.APIRouter()
        for r in router.routes:
            method = get_name(r.endpoint)
            operation_id = self.generate_operation_id_for_path(
                name=router.path, path=r.path, method=method
            )
            fastapi_api_router.add_api_route(
                r.path,
                r.endpoint,
                methods=[method],
                operation_id=operation_id,
                **r.kwargs
            )

        self.app.include_router(
            fastapi_api_router, prefix=router.path, tags=[router.name]
        )

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


class FastApiRouter(brev_route.Router):
    def __call__(self, fn=None):
        return super().__call__(fn=fn)