from hippie.interfaces import BaseCandidate

import numpy as np

class TSPAnt(BaseCandidate):
    """Represents problem as list of cities to visit in order."""

    def __init__(self, distance_matrix, pathfinding_alpha = 1, pathfinding_beta = 0, pathfinding_heuristic = None):
        self._path = None

        self.distance_matrix = distance_matrix
        self.len_path = self.distance_matrix.shape[0]

        self._all_cities = list(range(0, self.len_path))

        self.pathfinding_alpha = pathfinding_alpha
        self.pathfinding_beta = pathfinding_beta
        self.pathfinding_heuristic = pathfinding_heuristic

        pass

    def __str__(self):
        return str(self.cost)

    def generate_random_candidate(cls):
        return TSPAnt(None)

    def next_city_selector(self, current_city, unvisited_cities, pheromones):
        next_pheromones = np.zeros(self.len_path)

        for i in unvisited_cities:
            next_pheromones[i] = pheromones[current_city][i]

        tau_current_i_pow_alpha = np.array(next_pheromones ** self.pathfinding_alpha)
        eta_current_i_pow_beta = np.array(self.pathfinding_heuristic ** self.pathfinding_beta)
        tau_eta_array = tau_current_i_pow_alpha*eta_current_i_pow_beta

        next_probs = tau_eta_array / np.sum(tau_eta_array)  # probabilites to visit the next possible cities from the current city. Only not 0 for unvisited cities. Sums up to 1

        return np.random.choice(self._all_cities, p=next_probs)


    def find_path(self, pheromones):
        """Construct solution."""

        unvisited_cities = self._all_cities.copy()
        current_city = np.random.choice(unvisited_cities) #starts randomly at some city
        #current_city = 0  # or always choose city 0 to start. Should not make a difference, except the evaporator makes a difference for the index of the path

        unvisited_cities.remove(current_city)
        path = [current_city]

        while not len(unvisited_cities) == 0:

            next_city = self.next_city_selector(current_city, unvisited_cities, pheromones)
            path.append(next_city)
            unvisited_cities.remove(next_city)
            current_city = next_city
            print(path, end='\r')

        #path.append(path[0])
        self._path = path
        return path

    #def update_pheromone_matrix(self, pheromones):
    #    pheromones = pheromones

    @property
    def cost(self):
        if self._path == None:
            return -1000
        path_cost = 0
        for i in range(0, len(self._path)):
            path_cost += self.distance_matrix[self._path[i]][self._path[(i+1) % len(self._path)]]
        return path_cost

    def __getitem__(self, item):
        pass

    def __len__(self):
        pass
