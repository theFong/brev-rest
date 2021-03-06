import typing

from . import route
from . import rest


def nothing_app_handler(app: typing.Any) -> None:
    ...


Handler = typing.Callable[[typing.Any], None]


class Setup:
    is_setup = False

    arguments: rest.AppArgs = {
        "args": (),
        "kwargs": {},
    }

    routers_to_add: typing.List[route.Router] = []

    app_before_setup_handler = nothing_app_handler
    app_after_setup_handler = nothing_app_handler

    def __init__(
        self,
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> None:
        self.arguments["args"] = args
        self.arguments["kwargs"] = kwargs

        self.did_setup()

    def add_router(self, router: route.Router) -> None:
        self.routers_to_add.append(router)

    @classmethod
    def get_routers_to_add(cls) -> typing.List[route.Router]:
        if not cls.is_setup:
            raise Exception("Setup not setup")

        return cls.routers_to_add

    @classmethod
    def did_setup(cls):
        cls.is_setup = True

    @classmethod
    def app_before_setup(cls, handler: Handler):
        """
        Decorator
        """
        cls.app_before_setup_handler = handler
        return handler

    @classmethod
    def app_after_setup(cls, handler: Handler):
        """
        Decorator
        """
        cls.app_after_setup_handler = handler
        return handler
