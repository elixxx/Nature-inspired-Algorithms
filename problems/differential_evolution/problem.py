from problems.differential_evolution.de_candidate import *
ENERGY_PURCHASING_DEFAULT = 0.6

class Problem():

    def __init__(self, plants, markets, energy_purchasing_price=ENERGY_PURCHASING_DEFAULT):

        self._plants = plants
        self._markets = markets
        if energy_purchasing_price is None:
            self._energy_purchasing_price = ENERGY_PURCHASING_DEFAULT
        else:
            self._energy_purchasing_price = energy_purchasing_price

    def generate_list_of_random_candidates(self, number_of_candidates):

        list_of_candidates = [self.generate_random_candidate() for _ in range(number_of_candidates)]

        return list_of_candidates

    def generate_random_candidate(self):

        random_vector = self._construct_vector()

        new_candidate = self.generate_candidate(vector=random_vector)

        return new_candidate

    def generate_candidate(self, vector):

        new_candidate = Candidate(plants=self._plants, markets=self._markets,
                            energy_purchasing_price=self._energy_purchasing_price)

        new_candidate.set_vector(vector)

        return new_candidate

    def _construct_vector(self):

        random_energy_produced = np.array(
            [np.random.random(1)[0] * self._plants[i].max_planned_energy for i in range(len(self._plants))])
        random_planned_energy = np.array(
            [np.random.random(1)[0] * self._markets[i].max_demand for i in range(len(self._markets))])
        random_market_price = np.array(
            [np.random.random(1)[0] * self._markets[i].max_price for i in range(len(self._markets))])
        random_vector = np.concatenate((random_energy_produced, random_planned_energy, random_market_price), axis=0)
        return random_vector

    def __str__(self):
        return f'DE problem with {len(self._plants)} plants and {len(self._markets)} markets'