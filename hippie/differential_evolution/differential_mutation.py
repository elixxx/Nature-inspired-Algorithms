import hippie.interfaces as interfaces
import numpy as np
import copy


class DifferentialMutation(interfaces.BaseStrategy):

    def __init__(self, scaling_factor = 0.5):
        self._scaling_factor = scaling_factor

    def mutate(self, target, population):
        target_index = population.index(target)
        population_copy = copy.deepcopy(population)
        del(population_copy[target_index])
        base = np.random.choice(population_copy)
        population_copy.remove(base)
        x1 = np.random.choice(population_copy)
        population_copy.remove(x1)
        x2 = np.random.choice(population_copy)

        donor_vector = base.vector + self._scaling_factor * (x1.vector - x2.vector)

        return donor_vector

    @property
    def parameters(self):
        return {'scaling factor': self._scaling_factor}

    def __str__(self):
        return f'Scaling factor: {self._scaling_factor}'
