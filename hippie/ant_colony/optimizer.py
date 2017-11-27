import hippie.interfaces as interfaces
import numpy as np


class AntColonyOptimizer(interfaces.BaseOptimizer):

    def __init__(self, candidate_cls, distance_matrix, n_ants, initializer, evaporator, intensifier, convergence_criterion, pathfinding_alpha = 1, pathfinding_beta = 0, pathfinding_heuristic = None):

        self._distance_matrix = distance_matrix

        self._pathfinding_alpha = pathfinding_alpha
        self._pathfinding_beta = pathfinding_beta


        self._pheromones = initializer.initialize(self._distance_matrix.shape[0])
        #self._ants = [candidate_cls.initialize_random_candidate() for _ in range(n_ants)]
        self._ants = [candidate_cls.generate_random_candidate(distance_matrix = self._distance_matrix, pathfinding_alpha = self._pathfinding_alpha, pathfinding_beta = self._pathfinding_beta, pathfinding_heuristic = pathfinding_heuristic) for _ in range(n_ants)]
        self._evaporator = evaporator
        self._intensifier = intensifier
        self._convergence_criterion = convergence_criterion

    def plot_pheromones(self, pheromones):
        np.set_printoptions(threshold=np.nan)

        print(np.matrix(pheromones))

    def optimize(self):

        while not self._convergence_criterion.converged(self._ants, self._pheromones):
            for ant in self._ants:
                #ant.find_path()
                ant.find_path(self._pheromones) #Ants need the recent pheromone trails to generate their path

            self._pheromones = self._evaporator.evaporate(self._pheromones)

            self._pheromones = self._intensifier.intensify(self._ants, self._pheromones)

            #self.plot_pheromones(self._pheromones)

        return min(self._ants, key=lambda x: x.cost)

    def __str__(self):
        return str("{} ants with alpha {} and beta {}".format(len(self._ants), self._pathfinding_alpha, self._pathfinding_beta))

    def parameters(self):
        pass