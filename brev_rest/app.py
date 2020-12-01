import pathlib
from . import rest
from . import asgi
from . import loader
from . import route
from . import startup
from . import utils


def run(*, app_path: str) -> None:
    app = _make_app(app_path=app_path)
    app.run()


def get_server(*, app_path: str):
    app = _make_app(app_path=app_path)
    return app.get_server()


def _make_app(*, app_path: str) -> rest.App:
    loader.init_setup(app_path=app_path)
    routers = loader.make_routers(app_path=app_path)
    title = get_default_title(app_path=app_path)
    app = asgi.BrevFastApiApp(
        title=title,
        routers=routers,
        startup_args=startup.Setup.arguments,
        before_app_setup_handler=startup.Setup.app_before_setup_handler,
        after_app_setup_handler=startup.Setup.app_after_setup_handler,
    )
    return app


def get_default_title(*, app_path: str):
    raw_parent = pathlib.Path(app_path).parent.stem
    return raw_parent.replace("-", " ").replace("_", " ").capitalize()


def reset(*, app_path: str):
    route.Router.all_routers.clear()
    startup.Setup.arguments["args"] = ()
    startup.Setup.arguments["kwargs"] = {}
    startup.Setup.is_setup = False
    startup.Setup.routers_to_add.clear()
    utils.clear_modules(app_path)


def get_meta(*, app_path: str):
    app = _make_app(app_path=app_path)
    return app.get_meta()
