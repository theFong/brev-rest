import typing
import functools

all_routes: typing.List["Route"] = []  # temp singleton


class Route:
    def __init__(self, route_base: str, name: typing.Optional[str] = None):
        self.route_base = route_base

        if name is None:
            self.name = self.get_name_from_file()
        else:
            self.name = name
        self.fns: typing.List[typing.Callable] = []
        all_routes.append(self)

    def __call__(self, fn: typing.Union[typing.Callable]):
        if callable(fn):
            return self.decorator(fn)
        else:
            raise Exception("invalid decorator parameter")

    def decorator(self, fn: typing.Callable):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            return fn(*args, **kwargs)

        self.fns.append(fn)
        return inner

    @classmethod
    def get_name_from_file(cls):
        return __file__.split(".")[0]