import hippie.interfaces as interfaces


class Evaporator(interfaces.BaseStrategy):

    def __init__(self, rate):
        if not 0 < rate < 1:
            raise ValueError
        self._rate = rate

    def evaporate(self, pheromones):
        return (1 - self._rate) * pheromones

    @property
    def parameters(self):
        return {'evaporation_rate': self._rate}

    def __str__(self):
        return f'Evaporator rate={self._rate}'
