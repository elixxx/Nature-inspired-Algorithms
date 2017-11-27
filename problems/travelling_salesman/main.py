from hippie.ant_colony.initializer import *
from hippie.ant_colony.evaporator import *
from hippie.ant_colony.intensifier import *
from hippie.ant_colony.optimizer import *

from hippie.ant_colony.convergence import *
from problems.travelling_salesman.tsp_candidate import TSPAnt

from hippie.parser.parser import *

distance_matrix = parse_to_matrix("../../problems/travelling_salesman/data/1.tsp")

#distance_matrix = np.random.rand(1000, 1000)

initializer = ZeroInitializer()
evaporator = Evaporator(rate = 0.1)
intensifier = BestIntensifier(pheromone_increase = 5)
convergence_criterion = MaxIteration(1000)

n_ants = 20


antColonyOptimizer = AntColonyOptimizer(TSPAnt, distance_matrix=distance_matrix, n_ants=n_ants, initializer=initializer, evaporator=evaporator, intensifier=intensifier, convergence_criterion = convergence_criterion)
antColonyOptimizer.optimize()
#antColonyOptimizer.optimize_parallel()