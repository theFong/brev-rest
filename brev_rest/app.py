from . import rest
from . import asgi
from . import route_loader


def run(*, app_path: str, port=8000) -> None:
    routes = route_loader.make_routes(app_path=app_path)
    app = asgi.BrevFastApi(routes)

    _run(app)


def _run(rest_app: rest.App) -> None:
    rest_app.run()


def get_server(*, app_path: str):
    routes = route_loader.make_routes(app_path=app_path)
    app = asgi.BrevFastApi(routes)

    return _get_server(app)


def _get_server(rest_app: rest.App):
    return rest_app.get_server()
