from hippie.ant_colony.initializer import *
from hippie.ant_colony.evaporator import *
from hippie.ant_colony.intensifier import *
from hippie.ant_colony.optimizer import *

from hippie.ant_colony.convergence import *
from problems.travelling_salesman.tsp_candidate import HeuristicTSPAnt

from problems.travelling_salesman.parser import *
import datetime

start = datetime.datetime.now()
distance_matrix = parse_to_matrix("../../problems/travelling_salesman/data/1.tsp")

n_ants = 50
evaporation_rate = 0.3
pheromone_increase = 0.5
iterations = 10

initializer = ConstantInitializer(distance_matrix.shape[0], 1)

evaporator = Evaporator(rate=evaporation_rate )
intensifier = BestIntensifier(pheromone_increase=pheromone_increase)
convergence_criterion = MaxIteration(iterations)

ants = [HeuristicTSPAnt.generate_random_candidate(distance_matrix, pathfinding_alpha=1, pathfinding_beta=1)
        for _ in range(n_ants)]

antColonyOptimizer = AntColonyOptimizer(ants=ants,
                                        initializer=initializer, evaporator=evaporator,
                                        intensifier=intensifier,
                                        convergence_criterion=convergence_criterion)
optimal_run_result = antColonyOptimizer.optimize()

diff = datetime.datetime.now()-start
print(diff)

# for i in range(0, 100):
#     n_ants = np.random.randint(10, 120)
#     rand_rate = np.random.uniform(0, 1)
#     rand_pheromone_increase = np.random.uniform(0, 25)
#     iterations = np.random.randint(30, 400)
#
#     initializer = ZeroInitializer()
#     initializer = RandomInitializer()
#
#     evaporator = Evaporator(rate=rand_rate)
#     intensifier = BestIntensifier(pheromone_increase=rand_pheromone_increase)
#     convergence_criterion = MaxIteration(iterations)
#
#     ants = [TSPAnt.generate_random_candidate(distance_matrix) for _ in range(n_ants)]
#
#     antColonyOptimizer = AntColonyOptimizer(ants=ants,
#                                             initializer=initializer, evaporator=evaporator,
#                                             intensifier=intensifier,
#                                             convergence_criterion=convergence_criterion)
#     optimal_run_result = antColonyOptimizer.optimize()
#     print("Found result of path cost {} for {} ants, {} iterations, evaporator_rate={} and increase_rate={}".format(optimal_run_result.cost, n_ants, iterations, rand_rate, rand_pheromone_increase ))
#
#
# antColonyOptimizer = AntColonyOptimizer(TSPAnt, distance_matrix=distance_matrix, n_ants=n_ants,
#                                         initializer=initializer,
#                                         evaporator=evaporator, intensifier=intensifier,
#                                         convergence_criterion = convergence_criterion)
# antColonyOptimizer.optimize
#antColonyOptimizer.optimize_parallel()