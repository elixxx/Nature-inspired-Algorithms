import hippie.interfaces as interfaces
import numpy as np


class ZeroInitializer(interfaces.BaseStrategy):

    def __init__(self, dim):
        self._dim = dim

    def initialize(self):
        return np.zeros(shape=(self._dim, self._dim))

    @property
    def parameters(self):
        return {}

    def __str__(self):
        return 'ZeroInitializer'

class ConstantInitializer(interfaces.BaseStrategy):

    def __init__(self, dim, constant):
        self._dim = dim
        self._constant = constant

    def initialize(self):
        return np.ones(shape=(self._dim, self._dim)) * self._constant

    @property
    def parameters(self):
        return {}

    def __str__(self):
        return 'ZeroInitializer'

class RandomInitializer(interfaces.BaseStrategy):

    def __init__(self, dim):
        self._dim = dim

    def initialize(self):
        return np.random.rand(self._dim, self._dim)

    @property
    def parameters(self):
        return {}

    def __str__(self):
        return 'RandomInitializer'
