from operator import attrgetter

import hippie.interfaces as interfaces
import numpy as np


class AntColonyOptimizer(interfaces.BaseOptimizer):

    def __init__(self, ants, initializer, evaporator, intensifier,
                 convergence_criterion):
        self._pheromones = initializer.initialize()
        self._ants = ants
        self._evaporator = evaporator
        self._intensifier = intensifier
        self._convergence_criterion = convergence_criterion

    def plot_pheromones(self, pheromones):
        np.set_printoptions(threshold=np.nan)

        # print(np.matrix(pheromones))

    def optimize(self):
        iterations = 0
        while not self._convergence_criterion.converged(self._ants, self._pheromones):
            iterations += 1
            for ant in self._ants:
                ant.find_path(self._pheromones) #Ants need the recent pheromone trails to generate their path

            self._pheromones = self._evaporator.evaporate(self._pheromones)

            self._pheromones = self._intensifier.intensify(self._ants, self._pheromones)
            # print(iterations, self._pheromones)
            # print(self._pheromones.max())
            print("Iteration step {} of {}, lowest cost {}".format(iterations, self._convergence_criterion._n_max_iterations, min(self._ants, key=attrgetter('cost'))))

        return min(self._ants, key=attrgetter('cost'))

    def __str__(self):
        return f'Optimizer with {len(self._ants)} ants.'
    
    @property
    def parameters(self):
        return {'n_ants': len(self._ants),
                'evaporator': str(self._evaporator),
                'intensifier': str(self._intensifier),
                'convergence_criterion': str(self._convergence_criterion)}