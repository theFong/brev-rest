import abc
import typing

from .types import GenericKwargs

# AppArgs = typing.Dict[str, typing.Union[GenericArgs, GenericKwargs]]
AppArgs = typing.TypedDict(
    "AppArgs",
    {
        "args": typing.Tuple,
        "kwargs": GenericKwargs,
    },
)


class App(abc.ABC):
    @abc.abstractmethod
    def add_router(self, router: typing.Any) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def run(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_server(self) -> typing.Any:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_meta(self) -> typing.Dict[str, typing.Any]:
        raise NotImplementedError()
