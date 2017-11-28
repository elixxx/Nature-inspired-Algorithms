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

        print(np.matrix(pheromones))

    def optimize(self):
        iterations = 0
        while not self._convergence_criterion.converged(self._ants, self._pheromones):
            iterations += 1
            for ant in self._ants:
                ant.find_path(self._pheromones) #Ants need the recent pheromone trails to generate their path

            self._pheromones = self._evaporator.evaporate(self._pheromones)

            self._pheromones = self._intensifier.intensify(self._ants, self._pheromones)
            print(iterations, self._pheromones)
            print(self._pheromones.max())
            print("Iteration step {} of {}, lowest cost {}".format(iterations, self._convergence_criterion._n_max_iterations, min(self._ants, key=lambda x: x.cost)))

        return min(self._ants, key=lambda x: x.cost)

    def __str__(self):
        return str("{} ants with alpha {} and beta {}".format(len(self._ants), self._pathfinding_alpha, self._pathfinding_beta))

    def parameters(self):
        pass