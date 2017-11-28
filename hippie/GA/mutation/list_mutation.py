from ..base import *
import random
import numpy as np

class RandomMutation(BaseGAMutation):


    def __init__(self, pb, encoding_range):
        super().__init__(pb)
        self._encoding_range = encoding_range

    def call(self, candidate: Union[BaseGACandidate, Sequence]):
        for i, prop in enumerate(candidate):
            if random.random() < self._pb:
                candidate[i] = np.random.choice(list(range(self._encoding_range)))

    def __str__(self):
        return f'Mutation.RandomMutation'

    @property
    def parameters(self):
        return {'pb': self.pb, 'encoding_range': self._encoding_range}


class CreepMutation(BaseGAMutation):


    def __init__(self, pb, encoding_range):
        super().__init__(pb)
        self._encoding_range = encoding_range

    def call(self, candidate: Union[BaseGACandidate, Sequence]):
        for i, gene in enumerate(candidate):
            if random.random() < self._pb:
                candidate[i] = (
                    (candidate[i] + np.random.choice([-1, 1])) % self._encoding_range
                )

    def __str__(self):
        return f'Mutation.CreepMutation'

    @property
    def parameters(self):
        return {'pb': self.pb, 'encoding_range': self._encoding_range}
