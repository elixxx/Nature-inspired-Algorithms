from problems.travelling_salesman.tsp_candidate import *
from hippie.parser.parser import *
import numpy as np

distance_matrix = parse_to_matrix("../../problems/travelling_salesman/data/1.tsp")
distance_matrix = np.random.rand(1000, 1000)


len_path = distance_matrix.shape[0]

pheromones = np.random.rand(len_path, len_path)

ant = TSPAnt(distance_matrix, pathfinding_heuristic=np.zeros(len_path))
print(ant.find_path(pheromones))

print(ant.cost)