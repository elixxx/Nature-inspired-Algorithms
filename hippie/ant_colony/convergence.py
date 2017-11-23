
class MaxIteration:

    def __init__(self, n_max_iterations):
        self._iterations = 0
        self._n_max_iterations = n_max_iterations

    def converged(self, *args):
        if self._iterations == self._n_max_iterations:
            return True
        else:
            self._iterations += 1
