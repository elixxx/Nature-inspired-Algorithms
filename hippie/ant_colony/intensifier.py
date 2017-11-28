from operator import attrgetter

import hippie.interfaces as interfaces
import numpy as np


class BestIntensifier(interfaces.BaseStrategy):

    def __init__(self, pheromone_increase: float):
        self._pheromone_increase = pheromone_increase

    def intensify(self, ants, pheromones):

        best_ant = min(ants, key=attrgetter('cost'))

        #print("The best ant has a path cost of {} in comparison to the mean of {}".format(best_ant.cost, np.mean([x.cost for x in ants])))

        for i in range(len(best_ant) - 1):
            row = best_ant[i]
            col = best_ant[i + 1]
            pheromones[row, col] += self._pheromone_increase

        pheromones[best_ant[-1], best_ant[0]] += self._pheromone_increase

        return pheromones

    @property
    def parameters(self):
        return {'pheromone_increase_rate': self._pheromone_increase}

    def __str__(self):
        return f'Intensifier pheromone increase rate={self._pheromone_increase}'