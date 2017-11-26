from problems.travelling_salesman.tsp_candidate import *
from hippie.parser.parser import *
import pandas as pd
import numpy as np
from tqdm import tqdm
import time

def solve_tsp(path):
    distance_matrix = parse_to_matrix(path)
    #distance_matrix = np.random.rand(1000, 1000)
    len_path = distance_matrix.shape[0]
    pheromones = np.random.rand(len_path, len_path)
    ant = TSPAnt(distance_matrix, pathfinding_heuristic=np.zeros(len_path))
    return ant.find_path(pheromones), ant.cost

def experiment(path_list):
    frame = pd.DataFrame()
    names = list()
    costs = list()
    routes = list()
    for p in tqdm(path_list):
        route, cost = solve_tsp(p)
        names.append(p[-5:])
        costs.append(cost)
        routes.append(route)
        print(p[-5:], cost, route)
    frame['Name'] = pd.Series(names)
    frame['Cost'] = pd.Series(costs)
    frame['Route'] = pd.Series(routes)
    return frame

path_list = list()
path_list.append("problems/travelling_salesman/data/1.tsp")
path_list.append("problems/travelling_salesman/data/2.tsp")
path_list.append("problems/travelling_salesman/data/3.tsp")

results = experiment(path_list=path_list)
results.to_pickle("aco_"+str(time.time())+"log.pkl")

print("Finished")