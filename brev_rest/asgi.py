import typing
import abc
from starlette.types import ASGIApp
import fastapi
import uvicorn  # type: ignore


from . import rest
from . import route as brev_route


class Asgi(rest.App):
    @abc.abstractmethod
    def get_server(self) -> ASGIApp:
        raise NotImplementedError()


class BrevFastApi(Asgi):
    def __init__(self, routers: typing.List[brev_route.Router]):
        self.app = fastapi.FastAPI()

        for r in routers:
            self.add_router(r)

    def add_router(self, router: brev_route.Router):
        fastapi_api_router = fastapi.APIRouter()
        for r in router.routes:
            fastapi_api_router.add_api_route(
                r.path, r.endpoint, methods=[r.endpoint.__name__], *r.args, **r.kwargs
            )
        self.app.include_router(
            fastapi_api_router, prefix=router.path, tags=[router.name]
        )

    def get_server(self) -> ASGIApp:
        return self.app

    def run(self):
        uvicorn.run(self.app)


class FastApiRouter(brev_route.Router):
    def __call__(self, fn=None):
        return super().__call__(fn=fn)