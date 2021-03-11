import abc


class AbstractRepository:
    @abc.abstractmethod
    def get(self, id):
        pass

    @abc.abstractmethod
    def get_by(self, **kwargs):
        pass

    @abc.abstractmethod
    def all_by(self, **kwargs):
        pass

    @abc.abstractmethod
    def all(self):
        pass

    @abc.abstractmethod
    def add(self, entity):
        pass

    @abc.abstractmethod
    def update(self, entity):
        pass

    @abc.abstractmethod
    def remove(self, entity):
        pass

    @abc.abstractmethod
    def save(self):
        pass
