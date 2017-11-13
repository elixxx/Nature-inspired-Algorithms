from GA.iCandidate import ICandidate
from typing import List
class ISelection():

    def select(self, population: List[ICandidate]) -> List[ICandidate]:
        """
        Create a new population with len(population) candidates which
        :param population: old Population out of with the new one will get created
        :return: A new deep copied Population
        """
        raise NotImplementedError

class ICrossover():
    def call(self, parents :List[ICandidate], pb :float) -> List[ICandidate]:
        """
        Cross N Parents and create N new crossed Candidate
        :param parents: List of N parents, at the moment mostly just 2
        :param pb: probability for crossover
        :return: New generated Candidate len() = len(parents)
        """
        raise NotImplementedError

    @property
    def numParents(self) -> int:
        raise NotImplementedError

class IMutation():
    def call(self, candidate :ICandidate, pb :float) -> ICandidate:
        """
        Mutate a property of candidate for givven pb
        :param candidate: candidate which is calculated
        :param pb: probability for mutation
        :return:
        """
        raise NotImplementedError
