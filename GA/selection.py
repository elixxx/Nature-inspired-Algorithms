from GA.iOperations import ISelection
from GA import ICandidate
from typing import List
from sortedcontainers import SortedDict
import random
import copy
import numpy as np
import bisect


class RouletteWheel(ISelection):

    def __init__(self):
        pass


    def select(self, population: List[ICandidate]) -> List[ICandidate]:
        """
        Create a new population with len(population) candidates which
        :param population: old Population out of with the new one will get created
        :return: A new deep copied Population
        """
        cum_fit = 0
        fit_map = SortedDict()
        new_population = list()
        for i, cand in enumerate(population):
            fit_map[cum_fit]=cand
            # Max biggest fitness smalles, because we minimize
            cum_fit+=100/cand.cost
        for i in range(len(population)):
            rnd = random.uniform(0, cum_fit)
            index = fit_map.bisect(rnd)-1
            key = fit_map.iloc[index]
            new_population.append(copy.deepcopy(fit_map[key]))
        return new_population


class TournamentSelection(ISelection):
    def __init__(self, tournement_size, best_win_pb):
        self._tournement_size = tournement_size
        self._best_win_pb = best_win_pb

    def select(self, population: List[ICandidate]):
        new_population = list()
        if len(population) < self._tournement_size:
            raise ValueError("TournementSize bigger or equal populatinsize!")

        for i in range(len(population)):
            tournemant = np.random.choice(population, size=self._tournement_size, replace=False)
            tournemant = sorted(tournemant, key=lambda can:can.cost)
            if random.random() < self._best_win_pb:
                new_population.append(copy.deepcopy(tournemant[0]))
            else:
                new_population.append(copy.deepcopy(tournemant[-1]))

        return new_population
