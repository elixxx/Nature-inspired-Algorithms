import interfaces

class AntColonyOptimizer(interfaces.BaseOptimizer):

    def __init__(self, initializer, evaporizer, intensifier, convergence_criterion):
        self._pheromones = initializer.initialize()
        self._ants = []
        self._evaporizer = evaporizer
        self._intensifier = intensifier
        self._convergence_criterion = convergence_criterion
        self._previous_ants = None

    def optimize(self):

        while not self._convergence_criterion.is_met(self._ants, self._pheromones):
            for ant in self._ants:
                ant.find_path()

            self._pheromones = self._evaporizer(self._pheromones)

            self._pheromones = self._intensifier(self._ants, self._pheromones)

        return sorted(self._ants, key=lambda x: x.cost())[-1]

