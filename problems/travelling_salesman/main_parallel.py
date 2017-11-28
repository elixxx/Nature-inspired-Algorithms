import time
from tqdm import tqdm

from hippie.ant_colony.initializer import *
from hippie.ant_colony.evaporator import *
from hippie.ant_colony.intensifier import *
from hippie.ant_colony.optimizer import *

from hippie.ant_colony.convergence import *
from problems.travelling_salesman.tsp_candidate import TSPAnt, HeuristicTSPAnt

from hippie.parser.parser import *
from multiprocessing import Pool
import os

distance_matrix = parse_to_matrix("../../problems/travelling_salesman/data/1.tsp")
optimizer = list()

n_ants = 20

for i in range(0, 4):
    n_ants = np.random.randint(10, 100)
    rand_rate = np.random.uniform(0, 1)
    rand_pheromone_increase = np.random.uniform(0, 20)
    iterations = np.random.randint(1, 3)

    initializer = ConstantInitializer(distance_matrix.shape[0], 1)

    evaporator = Evaporator(rate=rand_rate)
    intensifier = BestIntensifier(pheromone_increase=5)
    convergence_criterion = MaxIteration(iterations)
    ants = [HeuristicTSPAnt.generate_random_candidate(distance_matrix, pathfinding_alpha=1, pathfinding_beta=1)
            for _ in range(n_ants)]
    antColonyOptimizer = AntColonyOptimizer(ants=ants,
                                            initializer=initializer, evaporator=evaporator,
                                            intensifier=intensifier,
                                            convergence_criterion=convergence_criterion)
    optimizer.append(antColonyOptimizer)
    # print("Found result of path cost {} for {} ants, {} iterations, evaporator_rate={} and increase_rate={}".format(optimal_run_result.cost, n_ants, iterations, rand_rate, rand_pheromone_increase ))

# e = Experiment.Worker(optimizer)
# e.start(0,20)
# e.get()
def call_optimize(x):
    return x.optimize()

p = Pool(len(os.sched_getaffinity(0)))
res = p.map_async(call_optimize,optimizer)
# for i in range
print(res)
while not res.ready():
    # frame = frame.append(f.get(), ignore_index=True)
    print(f'{res._number_left}/{len(optimizer)}')
    time.sleep(1)
res.get()
# antColonyOptimizer = AntColonyOptimizer(TSPAnt, distance_matrix=distance_matrix, n_ants=n_ants, initializer=initializer, evaporator=evaporator, intensifier=intensifier, convergence_criterion = convergence_criterion)
# antColonyOptimizer.optimize
#antColonyOptimizer.optimize_parallel()