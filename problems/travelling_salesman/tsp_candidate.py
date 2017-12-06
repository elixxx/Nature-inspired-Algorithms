from hippie.interfaces import BaseCandidate

import numpy as np
np.random.seed(0)

class TSPAnt(BaseCandidate):
    """Represents problem as list of cities to visit in order."""

    def __init__(self, distance_matrix, pathfinding_alpha = 1, pathfinding_beta = 0):
        self._path = None

        self.distance_matrix = distance_matrix
        self.len_path = self.distance_matrix.shape[0]

        self._all_cities = list(range(0, self.len_path))

        self.pathfinding_alpha = pathfinding_alpha
        self.pathfinding_beta = pathfinding_beta
        self._cost = None
        self.inverse_distance_matrix = 1 / self.distance_matrix
        self.inverse_distance_matrix[np.isinf(self.inverse_distance_matrix)] = 0

    def __str__(self):
        return f'TSPAnt with cost={self.cost}'

    @classmethod
    def generate_random_candidate(cls,**kwargs):

        return cls(kwargs['distance_matrix'], kwargs['pathfinding_alpha'], kwargs['pathfinding_beta'])

    def find_path(self, pheromones):
        """Construct solution."""

        unvisited_cities = self._all_cities.copy()
        current_city = np.random.choice(self._all_cities)
        unvisited_cities.remove(current_city)
        path = [current_city]

        while unvisited_cities:
            next_city = self.select_next_city(current_city, unvisited_cities, pheromones)
            path.append(next_city)
            unvisited_cities.remove(next_city)
            current_city = next_city
        # print(path)
        self._path = path


    def select_next_city(self, current_city, unvisited_cities, pheromones):

        next_pheromones = np.zeros(self.len_path)

        for i in unvisited_cities:
            next_pheromones[i] = pheromones[current_city][i]

        if sum(next_pheromones) == 0:
            #If all the pheromones are 0, only use the heuristic for a choice:
            tau_current_i_pow_alpha = next_pheromones
            tau_current_i_pow_alpha[unvisited_cities] = 1
        else:
            tau_current_i_pow_alpha = next_pheromones ** self.pathfinding_alpha


        eta_current_i_pow_beta = self.pathfinding_heuristic(current_city) ** self.pathfinding_beta

        tau_eta_array = tau_current_i_pow_alpha * eta_current_i_pow_beta

        # Probabilites to visit the next possible cities from the current city.
        # Only not 0 for unvisited cities. Sums up to 1
        next_probs = tau_eta_array / np.nansum(tau_eta_array)

        selected = np.random.choice(self._all_cities, p=next_probs)
        return selected

    def pathfinding_heuristic(self, current_city):
        return np.ones(self.len_path)

    @property
    def path(self):
        return self._path

    @property
    def cost(self):

        path_cost = 0

        for i in range(len(self._path)):
            path_cost += self.distance_matrix[self._path[i]][self._path[(i + 1) % len(self._path)]]

        self._cost = path_cost
        return self._cost

    def __getitem__(self, item):
        return self._path[item]

    def __len__(self):
        return self.len_path


class HeuristicTSPAnt(TSPAnt):

    def pathfinding_heuristic(self, current_city):
        return self.inverse_distance_matrix[current_city]

class LogicalTSPAnt(TSPAnt):
    def select_next_city(self, current_city, unvisited_cities, pheromones):

        next_pheromones = np.zeros(self.len_path)

        for i in unvisited_cities:
            next_pheromones[i] = pheromones[current_city][i]

        if sum(next_pheromones) == 0:
            #If all the pheromones are 0, only use the heuristic for a choice:
            tau_current_i_pow_alpha = next_pheromones
            tau_current_i_pow_alpha[unvisited_cities] = 1
        else:
            tau_current_i_pow_alpha = next_pheromones


        eta_current_i_pow_beta = self.pathfinding_heuristic(current_city) ** self.pathfinding_beta

        tau_eta_array = tau_current_i_pow_alpha * eta_current_i_pow_beta

        # Probabilites to visit the next possible cities from the current city.
        # Only not 0 for unvisited cities. Sums up to 1
        next_probs = tau_eta_array / np.nansum(tau_eta_array)

        selected = np.random.choice(self._all_cities, p=next_probs)
        return selected