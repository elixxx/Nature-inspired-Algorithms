import typing

class BaseCandidate(metaclass=typing.abc.ABCMeta):
    @property
    @typing.abc.abstractmethod
    def cost(self) -> float:
        pass

    @typing.abc.abstractmethod
    def __str__(self):
        pass

    @typing.abc.abstractclassmethod
    def generate_random_candidate(cls, **kwargs):
        pass

class BaseOptimizer(metaclass=typing.abc.ABCMeta):
    @typing.abc.abstractmethod
    def optimize(self):
        pass

    @typing.abstractmethod
    def __str__(self):
        pass

    @property
    @typing.abc.abstractmethod
    def parameters(self):
        pass


class BaseStrategy(metaclass=typing.abc.ABCMeta):
    @typing.abc.abstractmethod
    def __str__(self):
        pass

    @property
    @typing.abc.abstractmethod
    def parameters(self):
        pass