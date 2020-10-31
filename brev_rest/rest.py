import abc


class App(abc.ABC):
    @abc.abstractmethod
    def add_router(self, route):
        raise NotImplementedError()

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_server(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_meta(self):
        raise NotImplementedError()