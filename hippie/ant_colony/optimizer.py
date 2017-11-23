import hippie.interfaces as interfaces


class AntColonyOptimizer(interfaces.BaseOptimizer):

    def __init__(self, candidate_cls, n_ants, initializer, evaporator, intensifier, convergence_criterion):
        self._pheromones = initializer.initialize()
        self._ants = [candidate_cls.initialize_random_candidate() for _ in range(n_ants)]
        self._evaporator = evaporator
        self._intensifier = intensifier
        self._convergence_criterion = convergence_criterion

    def optimize(self):

        while not self._convergence_criterion.converged(self._ants, self._pheromones):
            for ant in self._ants:
                ant.find_path()

            self._pheromones = self._evaporator.evaporate(self._pheromones)

            self._pheromones = self._intensifier.intensify(self._ants, self._pheromones)

        return min(self._ants, key=lambda x: x.cost())

