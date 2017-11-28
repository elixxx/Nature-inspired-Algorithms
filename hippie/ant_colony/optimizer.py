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
        self.n_history = 9
        self.pheromone_history = np.dstack([initializer.initialize()] * self.n_history)
        self._optimize_val = None

    def plot_pheromones(self, pheromones):
        np.set_printoptions(threshold=np.nan)

        # print(np.matrix(pheromones))

    def optimize(self):
        iteration = 0
        step = np.floor(self._convergence_criterion.parameters['n_max_iterations'] / self.n_history)
        self.history_iter = [0]
        while not self._convergence_criterion.converged(self._ants, self._pheromones):
            iteration += 1
            for ant in self._ants:
                ant.find_path(self._pheromones) #Ants need the recent pheromone trails to generate their path

            self._pheromones = self._evaporator.evaporate(self._pheromones)

            self._pheromones = self._intensifier.intensify(self._ants, self._pheromones)

            if ((iteration % step) == 0):
                self.pheromone_history[..., len(self.history_iter) - 1] = self._pheromones
                self.history_iter.append(iteration)

            # print("Iteration step {} of {}, lowest cost {}".format(iteration, self._convergence_criterion._n_max_iterations, min(self._ants, key=attrgetter('cost'))))

        self._optimize_val = min(self._ants, key=attrgetter('cost'))
        return  self._optimize_val

    def __str__(self):
        return f'Optimizer with {len(self._ants)} ants.'

    def history(self):
        return self.pheromone_history, self.history_iter

    @property
    def parameters(self):
        return {'n_ants': len(self._ants),
                'evaporator': self._evaporator.parameters,
                'intensifier': self._intensifier.parameters,
                'convergence_criterion': self._convergence_criterion.parameters,
                'optimize_val': self._optimize_val}