import numpy as np
import math
from hippie.interfaces import BaseCandidate


class Candidate():

    def __init__(self, plants, markets, energy_purchasing_price):

        self._plants = plants
        self._markets = markets
        self._energy_purchasing_price = energy_purchasing_price

        self._vector = None
        self._energy_produced_vector = None
        self._planned_energy_vector = None
        self._market_price_vector = None
        self._profit = None

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
        return -self.profit

    @property
    def profit(self):
        self._profit = self.get_profit(self._energy_produced_vector, self._planned_energy_vector,
                                       self._market_price_vector)
        return self._profit

    # e = energy_produced, s = planned_energy, p = market price
    # Three vectors of equal length, |e| = |plants| and |s| = |p| = |markets\
    def get_profit(self, energy_produced, planned_energy, market_price):
        revenue = 0
        for market_price_i, planned_energy_i, market_i in zip(market_price, planned_energy, self._markets):
            if planned_energy_i < 0 or market_price_i < 0:
                return -math.inf
            revenue += min(market_i.demand(market_price_i), planned_energy_i) * market_price_i
            #print(f'new delta rev {min(market_i.demand(market_price_i), planned_energy_i) * market_price_i}')
            #print(f'new rev {revenue}')

        production_cost = 0
        for energy_produced_i, plant_i in zip(energy_produced, self._plants):
            production_cost += plant_i.cost(energy_produced_i)

        planned_energy_total = np.sum(planned_energy)
        energy_produced_total = np.sum(energy_produced)
        purchasing_cost = max(planned_energy_total - energy_produced_total, 0) * self._energy_purchasing_price

        cost = production_cost + purchasing_cost
        profit = revenue - cost
        return profit

    def __str__(self):
        return "Profit model for DE problem, vector: {}".format(self.vector)