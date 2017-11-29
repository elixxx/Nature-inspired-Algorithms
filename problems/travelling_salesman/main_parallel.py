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

ns_ants = [10,50]
evaporation_rates = [0.5, 0.7]
rand_pheromone_increases = [0.5]
iterations = 1
number_experiments = 10
pathfinding_alphas = [0, 1]
pathfinding_betas = [0, 1]
for rand_pheromone_increase in rand_pheromone_increases:
    for evaporation_rate in evaporation_rates:
        for n_ants in ns_ants:
            for i in range(number_experiments):
                for pathfinding_alpha in pathfinding_alphas:
                    for pathfinding_beta  in pathfinding_betas:
                        if pathfinding_beta ==0 and pathfinding_alpha==0:
                            continue
                        initializer = ConstantInitializer(distance_matrix.shape[0], 1)

                        evaporator = Evaporator(rate=evaporation_rate)
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

p = Pool(len(os.sched_getaffinity(0)))
# p =Pool(1)
# res = p.map_async(call_optimize,optimizer)
optimized = list()
for opt in optimizer:
    optimized.append(p.apply_async(opt.optimize))

number_of_experiments = len(optimizer)
print(f'{number_of_experiments} on {len(os.sched_getaffinity(0))} cores')
optimizer = list()
for f in tqdm(optimized):
    optimizer.append(f.get())

p.close()
p.join()

frame = pd.DataFrame()
for idx, opt in enumerate(optimizer):
    fl = flatten(opt.parameters)
    fl["experiment_id"] = idx
    fl["problem"] = problem
    fl["optimize_value_cost"] = opt.optimze_value.cost
    fl["optimize_value_path"] = opt.optimze_value.path
    fl["optimizer_instance"] = opt
    frame = frame.append(pd.DataFrame([fl], columns=fl.keys()))
frame.to_pickle(str(datetime.now().timestamp())+"out.pkl")