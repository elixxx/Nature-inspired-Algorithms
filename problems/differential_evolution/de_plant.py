import math

"""We describe each plant type by three parameters
k - kWh per plant
c - cost per plant
m - maximum number of plants that can be used
"""

class PlantType():

    def __init__(self, kwh_per_plant, cost_per_plant, max_number_of_plants, large_value = math.inf):
        self._kwh_per_plant = kwh_per_plant
        self._cost_per_plant = cost_per_plant
        self._max_number_of_plants = max_number_of_plants
        self._large_value = math.inf

    def cost(self, x):
        #if x is non-positive, return 0
        if x <= 0:
            return 0

        #if x i greater than hat can be generated return prohibitively large value
        if x > (self._kwh_per_plant * self._max_number_of_plants):
            return self._large_value

        #otherwise determine number of plants needed to generate x
        plants_needed = math.ceil(x / self._kwh_per_plant)

        return plants_needed * self._cost_per_plant