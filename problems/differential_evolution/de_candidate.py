import numpy as np
from hippie.interfaces import BaseCandidate

class Profitmodel(BaseCandidate):
    def __init__(self, plants, markets, energy_purchasing_price = 0.6):
        self._plants = plants
        self._markets = markets
        self._energy_purchasing_price = energy_purchasing_price

    def __str__(self):
        return "Profit model for DE problem"

    @classmethod
    def generate_random_candidate(cls, **kwargs):
        return None


    @property
    def cost(self):
        #cant define cost without more information
        return 0

    # e = energy_produced, s = planned_energy, p = market price
    # Three vectors of equal length, |e| = |plants| and |s| = |p| = |markets\
    def profit(self, energy_produced, planned_energy, market_price):
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
        profit =  revenue - cost
        return profit