import hippie.interfaces as interfaces
import numpy as np

class ZeroInitializer(interfaces.BaseStrategy):


    def initialize(self, dim):
        return np.ones(shape=(dim, dim))
        #return np.zeros(shape=(dim, dim))

    @property
    def parameters(self):
        return {}

    def __str__(self):
        return 'ZeroInitializer'