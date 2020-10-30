import pathlib
from . import rest
from . import asgi
from . import loader
from . import route
from . import startup
from . import utils


def run(*, app_path: str) -> None:
    loader.init_setup(app_path=app_path)
    routes = loader.make_routers(app_path=app_path)
    title = get_default_title(app_path=app_path)
    app = asgi.BrevFastApiApp(
        title=title,
        routers=routes,
        startup_args=startup.Setup.arguments,
        before_app_setup_handler=startup.Setup.app_before_setup_handler,
        after_app_setup_handler=startup.Setup.app_after_setup_handler,
    )

    _run(app)


def _run(rest_app: rest.App) -> None:
    rest_app.run()


def get_server(*, app_path: str):
    loader.init_setup(app_path=app_path)
    routers = loader.make_routers(app_path=app_path)
    print(routers)
    print(len(routers))
    title = get_default_title(app_path=app_path)
    app = asgi.BrevFastApiApp(
        title=title,
        routers=routers,
        startup_args=startup.Setup.arguments,
        before_app_setup_handler=startup.Setup.app_before_setup_handler,
        after_app_setup_handler=startup.Setup.app_after_setup_handler,
    )

    return _get_server(app)


def get_default_title(*, app_path: str):
    raw_parent = pathlib.Path(app_path).parent.stem
    return raw_parent.replace("-", " ").replace("_", " ").capitalize()


def _get_server(rest_app: rest.App):
    return rest_app.get_server()


def reset(*, app_path):
    route.Router.all_routers.clear()
    startup.Setup.arguments["args"] = {}
    startup.Setup.arguments["kwargs"] = {}
    startup.Setup.is_setup = False
    startup.Setup.routers_to_add.clear()
    utils.clear_modules(app_path)
