import typing
import functools
import inspect
import pathlib
from dataclasses import dataclass


default_sub_path = ""


@dataclass
class Route:
    endpoint: typing.Callable
    args: typing.Tuple[typing.Any]
    kwargs: typing.Any
    path: str = default_sub_path


class Router:
    all_routers: typing.List["Router"] = []  # temp singleton

    def __init__(self, path: str, name: typing.Optional[str] = None, **kwargs):
        self.path = path

        self.kwargs = kwargs

        if name is None:
            self.name = self.get_name_from_file()
        else:
            self.name = name

        self.routes: typing.List[Route] = []
        self.all_routers.append(self)

    def __call__(
        self,
        endpoint: typing.Callable = None,  # must be first argument
        path: str = default_sub_path,
        *args,
        **kwargs
    ):
        """
        Decorator
        """

        def decorator(_endpoint):
            @functools.wraps(_endpoint)
            def inner(*args, **kwargs):
                return endpoint(*args, **kwargs)

            route = Route(path=path, endpoint=_endpoint, args=args, kwargs=kwargs)
            self.routes.append(route)
            return inner

        if callable(endpoint):
            return decorator(endpoint)
        elif endpoint is None:
            return decorator
        else:
            raise Exception("Invalid argument", endpoint)

    @classmethod
    def get_name_from_file(cls):
        frame = inspect.stack()[2]
        name = pathlib.Path(frame.filename).stem
        return name

    @classmethod
    def get_all_routers(cls):
        return cls.all_routers
