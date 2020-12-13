import typing
import functools
import inspect
import pathlib
from dataclasses import dataclass

from .types import AnyKwargs, AnyCallable


default_sub_path = ""


@dataclass
class Route:
    endpoint: typing.Callable[..., typing.Any]
    args: typing.Tuple
    kwargs: AnyKwargs
    path: str = default_sub_path


T = typing.TypeVar("T", bound=AnyCallable)


class Router:
    all_routers: typing.List["Router"] = []  # temp singleton

    def __init__(
        self, path: str, name: typing.Optional[str] = None, **kwargs: typing.Any
    ):
        self.path = path

        self.kwargs: AnyKwargs = kwargs

        if name is None:
            self.name = self.get_name_from_file()
        else:
            self.name = name

        self.routes: typing.List[Route] = []
        self.all_routers.append(self)

    def __call__(
        self,
        endpoint: T = None,  # must be first argument
        path: str = default_sub_path,
        *args: typing.Any,
        **kwargs: typing.Any
    ) -> typing.Union[T, typing.Callable[[T], T]]:
        """
        Decorator
        """

        def decorator(_endpoint: T):
            @functools.wraps(_endpoint)
            def inner(*args: typing.Any, **kwargs: typing.Any):
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
        frame = inspect.stack()[3]
        name = pathlib.Path(frame.filename).stem
        return name.capitalize()

    @classmethod
    def get_all_routers(cls):
        return cls.all_routers
