import hippie.interfaces as interfaces
import numpy as np


class Crossover(interfaces.BaseStrategy):

    def __init__(self, crossover_rate):
        self._crossover_rate = crossover_rate

    def crossover(self, target_vector, donor_vector):
        r = np.random.randint(len(target_vector))
        trial_vector = np.zeros(len(target_vector))

        for i in range(len(target_vector)):
            if np.random.rand() <= self._crossover_rate:
                trial_vector[i] = donor_vector[i]
            elif i == r:
                trial_vector[i] = donor_vector[i]
            else:
                trial_vector[i] = target_vector[i]

        return trial_vector

    @property
    def parameters(self):
        return {'crossover_rate': self._crossover_rate}

    def __str__(self):
        return f'Crossover rate: {self._crossover_rate}'
