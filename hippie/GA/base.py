from interfaces import BaseCandidate
from typing import List, Union, Sequence
import interfaces


class BaseGACandidate(BaseCandidate):

    def diversity(self, other):
        raise NotImplementedError

class BaseGASelection(interfaces.BaseStrategy):

    def select(self, population: List[BaseGACandidate]) -> List[BaseGACandidate]:
        """
        Create a new population with len(population) candidates which
        :param population: old Population out of with the new one will get created
        :return: A new deep copied Population
        """
        raise NotImplementedError


class BaseGACrossover(interfaces.BaseStrategy):
    def __init__(self, pb):
        self._pb = pb

    @property
    def pb(self):
        return self._pb

    def call(self, parents: List[Union[BaseGACandidate, Sequence]]):
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


class BaseGAMutation(interfaces.BaseStrategy):
    def __init__(self, pb):
        self._pb = pb

    @property
    def pb(self):
        return self._pb

    def call(self, candidate: Union[BaseGACandidate, Sequence]):
        """
        Mutate a property of candidate for givven pb
        :param candidate: candidate which is calculated
        :param pb: probability for mutation
        :return:
        """
        raise NotImplementedError
