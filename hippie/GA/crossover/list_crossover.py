from ..base import *
import random


class OnePointCross(BaseGACrossover):

    def __init__(self, pb):
        super().__init__(pb)

    def numParents(self):
        return 2

    def call(self, parents :List[Union[BaseGACandidate, Sequence]]) -> List[Union[BaseGACandidate, Sequence]]:
        if len(parents) != 2:
            print("onePointCross takes only 2 parents")
            raise ValueError
        if random.random() > self._pb:
            return parents
        sol_length = len(parents[0])
        cut = random.randint(1,sol_length)
        tmp = parents[0][0:cut]
        parents[0][0:cut] = parents[1][0:cut]
        parents[1][0:cut] = tmp
        return parents

    def __str__(self):
        return f'Crossover.OnePointCross'

    @property
    def parameters(self):
        return {'pb': self.pb}


class TwoPointCross(BaseGACrossover):

    def __init__(self, pb):
        super().__init__(pb)

    def numParents(self):
        return 2

    def call(self, parents :List[Union[BaseGACandidate, Sequence]]) -> List[Union[BaseGACandidate, Sequence]]:
        if len(parents) != 2:
            print("onePointCross takes only 2 parents")
            raise ValueError
        if random.random() > self._pb:
            return parents
        sol_length = len(parents[0])
        cut_start = random.randint(1, sol_length)
        cut_end = random.randint(cut_start,sol_length)
        tmp = parents[0][cut_start:cut_end]
        parents[0][cut_start:cut_end] = parents[1][cut_start:cut_end]
        parents[1][cut_start:cut_end] = tmp
        return parents

    def __str__(self):
        return f'Crossover.TwoPointCross'

    @property
    def parameters(self):
        return {'pb': self.pb}