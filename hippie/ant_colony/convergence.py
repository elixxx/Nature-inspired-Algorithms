from hippie.interfaces import BaseStrategy

class MaxIteration(BaseStrategy):

    def __init__(self, n_max_iterations):
        self._iterations = 0
        self._n_max_iterations = n_max_iterations

    def converged(self, *args):
        if self._iterations == self._n_max_iterations:
            return True
        else:
            self._iterations += 1

    def __str__(self):
        return f'{self.__class__.__name__} with {self._n_max_iterations} iterations'

    @property
    def prameters(self):
        return {'n_max_iterations': self._n_max_iterations}