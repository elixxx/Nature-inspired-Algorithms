from hippie.ant_colony.initializer import *
from hippie.ant_colony.evaporator import *
from hippie.ant_colony.intensifier import *
from hippie.ant_colony.optimizer import *

from hippie.ant_colony.convergence import *
from problems.travelling_salesman.tsp_candidate import TSPAnt

from hippie.parser.parser import *

distance_matrix = parse_to_matrix("../../problems/travelling_salesman/data/1.tsp")

n_ants = 50
rand_rate = 0.3
rand_pheromone_increase = 10
iterations = 1000

initializer = RandomInitializer()

evaporator = Evaporator(rate=rand_rate)
intensifier = BestIntensifier(pheromone_increase=rand_pheromone_increase)
convergence_criterion = MaxIteration(iterations)

antColonyOptimizer = AntColonyOptimizer(TSPAnt, distance_matrix=distance_matrix, n_ants=n_ants,
                                        initializer=initializer, evaporator=evaporator, intensifier=intensifier,
                                        convergence_criterion=convergence_criterion)
optimal_run_result = antColonyOptimizer.optimize

for i in range(0, 100):
    n_ants = np.random.randint(10, 120)
    rand_rate = np.random.uniform(0, 1)
    rand_pheromone_increase = np.random.uniform(0, 25)
    iterations = np.random.randint(30, 400)

    initializer = ZeroInitializer()
    initializer = RandomInitializer()

    evaporator = Evaporator(rate=rand_rate)
    intensifier = BestIntensifier(pheromone_increase=rand_pheromone_increase)
    convergence_criterion = MaxIteration(iterations)

    antColonyOptimizer = AntColonyOptimizer(TSPAnt, distance_matrix=distance_matrix, n_ants=n_ants,
                                            initializer=initializer, evaporator=evaporator, intensifier=intensifier,
                                            convergence_criterion=convergence_criterion)
    optimal_run_result = antColonyOptimizer.optimize
    print("Found result of path cost {} for {} ants, {} iterations, evaporator_rate={} and increase_rate={}".format(optimal_run_result.cost, n_ants, iterations, rand_rate, rand_pheromone_increase ))


antColonyOptimizer = AntColonyOptimizer(TSPAnt, distance_matrix=distance_matrix, n_ants=n_ants, initializer=initializer, evaporator=evaporator, intensifier=intensifier, convergence_criterion = convergence_criterion)
antColonyOptimizer.optimize
#antColonyOptimizer.optimize_parallel()