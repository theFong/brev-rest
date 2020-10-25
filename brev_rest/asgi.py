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
    def __init__(self, routes: typing.List[brev_route.Route]):
        self.app = fastapi.FastAPI()

        for r in routes:
            self.add_route(r)

    def add_route(self, route: brev_route.Route):
        for fn in route.fns:
            self.app.add_api_route(route.route_base, fn, methods=[fn.__name__])

    def add_route_group(self, group):
        raise NotImplementedError()

    def get_server(self) -> ASGIApp:
        return self.app

    def run(self):
        uvicorn.run(self.app)