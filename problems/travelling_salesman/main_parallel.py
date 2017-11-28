from hippie.ant_colony.initializer import *
from hippie.ant_colony.evaporator import *
from hippie.ant_colony.intensifier import *
from hippie.ant_colony.optimizer import *

from hippie.ant_colony.convergence import *
from problems.travelling_salesman.tsp_candidate import TSPAnt

from hippie.parser.parser import *

distance_matrix = parse_to_matrix("../../problems/travelling_salesman/data/1.tsp")

initializer = ZeroInitializer()
evaporator = Evaporator(rate = 0.1)
intensifier = BestIntensifier(pheromone_increase = 5)
convergence_criterion = MaxIteration(300)

n_ants = 20

for i in range(0, 20):
    n_ants = np.random.randint(10, 100)
    rand_rate = np.random.uniform(0, 1)
    rand_pheromone_increase = np.random.uniform(0, 20)
    iterations = np.random.randint(20, 200)

    initializer = ZeroInitializer()

    evaporator = Evaporator(rate=rand_rate)
    intensifier = BestIntensifier(pheromone_increase=5)
    convergence_criterion = MaxIteration(iterations)

    antColonyOptimizer = AntColonyOptimizer(TSPAnt, distance_matrix=distance_matrix, n_ants=n_ants,
                                            initializer=initializer, evaporator=evaporator, intensifier=intensifier,
                                            convergence_criterion=convergence_criterion)
    optimal_run_result = antColonyOptimizer.optimize_parallel()
    print("Found result of path cost {} for {} ants, {} iterations, evaporator_rate={} and increase_rate={}".format(optimal_run_result.cost, n_ants, iterations, rand_rate, rand_pheromone_increase ))


antColonyOptimizer = AntColonyOptimizer(TSPAnt, distance_matrix=distance_matrix, n_ants=n_ants, initializer=initializer, evaporator=evaporator, intensifier=intensifier, convergence_criterion = convergence_criterion)
antColonyOptimizer.optimize
#antColonyOptimizer.optimize_parallel()