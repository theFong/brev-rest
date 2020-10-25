import abc


class App(abc.ABC):
    @abc.abstractmethod
    def add_route(self, route):
        raise NotImplementedError()

    @abc.abstractmethod
    def add_route_group(self, group):
        raise NotImplementedError()

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_server(self):
        raise NotImplementedError()
