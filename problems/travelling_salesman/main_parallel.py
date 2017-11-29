import time
from tqdm import tqdm
import pandas as pd
from hippie.ant_colony.initializer import *
from hippie.ant_colony.evaporator import *
from hippie.ant_colony.intensifier import *
from hippie.ant_colony.optimizer import *

from hippie.ant_colony.convergence import *
from problems.travelling_salesman.tsp_candidate import TSPAnt, HeuristicTSPAnt

from hippie.parser.parser import *
from multiprocessing import Pool
import os
import collections
def flatten(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

problem = "1.tsp"
distance_matrix = parse_to_matrix("../../problems/travelling_salesman/data/"+problem)
optimizer = list()
iterations = 2
for i in range(0, 3):
    n_ants = np.random.randint(10, 100)
    rand_rate = np.random.uniform(0, 1)
    rand_pheromone_increase = np.random.uniform(0, 20)


    initializer = ConstantInitializer(distance_matrix.shape[0], 1)

    evaporator = Evaporator(rate=rand_rate)
    intensifier = BestIntensifier(pheromone_increase=rand_pheromone_increase)
    convergence_criterion = MaxIteration(iterations)
    ants = [HeuristicTSPAnt.generate_random_candidate(distance_matrix, pathfinding_alpha=1, pathfinding_beta=1)
            for _ in range(n_ants)]
    antColonyOptimizer = AntColonyOptimizer(ants=ants,
                                            initializer=initializer, evaporator=evaporator,
                                            intensifier=intensifier,
                                            convergence_criterion=convergence_criterion)
    optimizer.append(antColonyOptimizer)


def call_optimize(x):
    return x.optimize()

p = Pool(len(os.sched_getaffinity(0)))
res = p.map_async(call_optimize,optimizer)
number_of_experiments = len(optimizer)

for i in tqdm(range(number_of_experiments)):
    num = res._number_left
    while num == res._number_left and not res.ready():
        time.sleep(1)
res.wait()
p.close()

optimizer = res.get()

frame = pd.DataFrame()
for opt in optimizer:
    fl = flatten(opt.parameters)
    fl["problem"] = problem
    fl["optimize_value"] = opt.optimze_value
    frame = frame.append(pd.DataFrame([fl], columns=fl.keys()))
frame.to_pickle("out.pkl")