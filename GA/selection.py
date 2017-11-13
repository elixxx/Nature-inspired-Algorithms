from GA.iOperations import ISelection
from GA import ICandidate
from typing import List
from sortedcontainers import SortedDict
import random
import copy
import bisect
class RouletWheel(ISelection):


    def __init__(self):
        pass


    def select(self, population: List[ICandidate]) -> List[ICandidate]:
        """
        Create a new population with len(population) candidates which
        :param population: old Population out of with the new one will get created
        :return: A new deep copied Population
        """
        cumFit = 0
        fitMap = SortedDict()
        newPopulation = list()
        for i, cand in enumerate(population):
            fitMap[cumFit]=cand
            # Max biggest fitness smalles, because we minimize
            cumFit+=1/cand.cost
        for i in range(len(population)):
            rnd = random.uniform(0, cumFit)
            index = fitMap.bisect(rnd)-1
            key = fitMap.iloc[index]
            newPopulation.append(copy.deepcopy(fitMap[key]))
        return newPopulation