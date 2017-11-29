import time

from datetime import date, datetime
from tqdm import tqdm
import pandas as pd
from hippie.ant_colony.initializer import *
from hippie.ant_colony.evaporator import *
from hippie.ant_colony.intensifier import *
from hippie.ant_colony.optimizer import *

from hippie.ant_colony.convergence import *
from problems.travelling_salesman.tsp_candidate import TSPAnt, HeuristicTSPAnt, LogicalTSPAnt

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

ns_ants = [10, 20]
rand_rates = [0.5, 0.7]
rand_pheromone_increases = [5, 10, 20]
iterations = 2
number_experiments = 1
pathfinding_alphas = [0, 1]
pathfinding_betas = [0, 1]
for rand_pheromone_increase in rand_pheromone_increases:
    for rand_rate in rand_rates:
        for n_ants in ns_ants:
            for i in range(number_experiments):
                for pathfinding_alpha in pathfinding_alphas:
                    for pathfinding_beta  in pathfinding_betas:
                        initializer = ConstantInitializer(distance_matrix.shape[0], 1)

                        evaporator = Evaporator(rate=rand_rate)
                        intensifier = BestIntensifier(pheromone_increase=rand_pheromone_increase)
                        convergence_criterion = MaxIteration(iterations)
                        ants = [LogicalTSPAnt.generate_random_candidate(distance_matrix,
                                                                          pathfinding_alpha=pathfinding_alpha,
                                                                          pathfinding_beta=pathfinding_beta)
                                for _ in range(n_ants)]
                        antColonyOptimizer = AntColonyOptimizer(ants=ants,
                                                                initializer=initializer, evaporator=evaporator,
                                                                intensifier=intensifier,
                                                                convergence_criterion=convergence_criterion)
                        optimizer.append(antColonyOptimizer)


def call_optimize(x):
    ret = None
    try:
        ret = x.optimize()
    except Exception as e:
        print(e)
        print(x.parameters)
    return ret

# p = Pool(len(os.sched_getaffinity(0)))
p =Pool(1)
res = p.map_async(call_optimize,optimizer)
number_of_experiments = len(optimizer)
print(f'{number_of_experiments} on {len(os.sched_getaffinity(0))} cores')
for i in tqdm(range(number_of_experiments)):
    num = res._number_left
    while num == res._number_left and not res.ready():
        time.sleep(1)
res.wait()
p.close()

optimizer = res.get()

frame = pd.DataFrame()
for idx, opt in enumerate(optimizer):
    fl = flatten(opt.parameters)
    fl["experiment_id"] = idx
    fl["problem"] = problem
    fl["optimize_value"] = opt.optimze_value
    fl["optimizer_instance"] = opt
    frame = frame.append(pd.DataFrame([fl], columns=fl.keys()))
frame.to_pickle(str(datetime.now().timestamp())+"out.pkl")