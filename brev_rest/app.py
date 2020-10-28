import pathlib
from . import rest
from . import asgi
from . import route_loader
from . import route


def run(*, app_path: str) -> None:
    routes = route_loader.make_routes(app_path=app_path)
    title = get_default_title(app_path=app_path)
    app = asgi.BrevFastApi(title, routes)

    _run(app)


def _run(rest_app: rest.App) -> None:
    rest_app.run()


def get_server(*, app_path: str):
    routes = route_loader.make_routes(app_path=app_path)
    title = get_default_title(app_path=app_path)
    app = asgi.BrevFastApi(title, routes)

    return _get_server(app)


def get_default_title(*, app_path: str):
    raw_parent = pathlib.Path(app_path).parent.stem
    return raw_parent.replace("-", " ").replace("_", " ").capitalize()


def _get_server(rest_app: rest.App):
    return rest_app.get_server()


def reset():
    route.all_routes = []
