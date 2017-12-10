import numpy as np
from hippie.interfaces import BaseCandidate

ENERGY_PURCHASING_DEFAULT = 0.6


class Profitmodel(BaseCandidate):
    def __init__(self, plants, markets, energy_purchasing_price=ENERGY_PURCHASING_DEFAULT):

        self._plants = plants
        self._markets = markets
        if energy_purchasing_price is None:
            self._energy_purchasing_price = ENERGY_PURCHASING_DEFAULT
        else:
            self._energy_purchasing_price = energy_purchasing_price

        self._vector = None
        self._energy_produced_vector = None
        self._planned_energy_vector = None
        self._market_price_vector = None
        self._profit = None

    def __str__(self):
        return "Profit model for DE problem, vector: {}".format(self.vector)

    @classmethod
    def generate_random_candidate(cls, **kwargs):

        random_energy_produced = np.array(np.random.random(len(kwargs['plants'])))

        random_energy_produced = np.array(
            [np.random.random(1)[0] * kwargs['plants'][i].max_planned_energy for i in range(len(kwargs['plants']))])
        # test = kwargs['plants'].max_planned_energy


        random_planned_energy = np.array(np.random.random(len(kwargs['markets'])+1))
        random_planned_energy = np.array(
            [np.random.random(1)[0] * kwargs['markets'][i].max_demand for i in range(len(kwargs['markets']))])
        random_market_price = np.array(np.random.random(len(kwargs['markets'])))
        random_market_price = np.array(
            [np.random.random(1)[0] * kwargs['markets'][i].max_price for i in range(len(kwargs['markets']))])
        random_vector = np.concatenate((random_energy_produced, random_planned_energy, random_market_price), axis=0)

        new_candidate = cls.generate_candidate(**kwargs, vector=random_vector)

        return new_candidate

    @classmethod
    def generate_candidate(cls, **kwargs):

        if not 'energy_purchasing_price' in kwargs.keys():
            energy_purchasing_price = ENERGY_PURCHASING_DEFAULT
        else:
            energy_purchasing_price = kwargs['energy_purchasing_price']

        new_candidate = cls(plants=kwargs['plants'], markets=kwargs['markets'],
                            energy_purchasing_price=energy_purchasing_price)

        if not 'vector' in kwargs.keys():
            return None
        else:
            new_candidate.set_vector(kwargs['vector'])

        return new_candidate

    @property
    def vector(self):
        return self._vector

    def set_vector(self, new_vector):
        self.set_energy_produced(new_vector[0:len(self._plants)])
        self.set_planned_energy(new_vector[len(self._plants):(len(self._plants) + len(self._markets))])
        self.set_market_price(new_vector[(len(self._plants) + len(self._markets)):(
        len(self._plants) + len(self._markets) + len(self._markets))])
        self._vector = np.concatenate((self._energy_produced_vector, self._planned_energy_vector,
                                      self._market_price_vector))

    def set_energy_produced(self, new_energy_produced):
        self._energy_produced_vector = new_energy_produced

    def set_planned_energy(self, new_planned_energy):
        self._planned_energy_vector = new_planned_energy

    def set_market_price(self, new_market_price):
        self._market_price_vector = new_market_price

    @property
    def cost(self):
        self._cost = -self.profit(self._energy_produced_vector, self._planned_energy_vector, self._market_price_vector)
        return self._cost

    @property
    def profit(self):
        self._profit = self.get_profit(self._energy_produced_vector, self._planned_energy_vector,
                                       self._market_price_vector)
        return self._profit

    # def profit(self):
    #   return self.profit(self._energy_produced_vector, self._planned_energy_vector, self._market_price_vector)

    # e = energy_produced, s = planned_energy, p = market price
    # Three vectors of equal length, |e| = |plants| and |s| = |p| = |markets\
    def get_profit(self, energy_produced, planned_energy, market_price):
        revenue = 0
        for market_price_i, planned_energy_i, market_i in zip(market_price, planned_energy, self._markets):
            revenue += min(market_i.demand(market_price_i), planned_energy_i) * market_price_i

        production_cost = 0
        for energy_produced_i, plant_i in zip(energy_produced, self._plants):
            production_cost += plant_i.cost(energy_produced_i)

        planned_energy_total = np.sum(planned_energy)
        energy_produced_total = np.sum(energy_produced)
        purchasing_cost = max(planned_energy_total - energy_produced_total, 0) * self._energy_purchasing_price

        cost = production_cost + purchasing_cost
        profit = revenue - cost
        return profit
