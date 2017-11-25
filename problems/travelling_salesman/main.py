from hippie.ant_colony.initializer import *
from hippie.ant_colony.evaporator import *
from hippie.ant_colony.intensifier import *
from hippie.ant_colony.optimizer import *

from hippie.ant_colony.convergence import *
from problems.travelling_salesman.tsp_candidate import TSPAnt


initializer = ZeroInitializer()
evaporator = Evaporator(rate = 0.1)
intensifier = BestIntensifier(pheromone_increase = 0.1)
convergence_criterion = MaxIteration(20)

antColonyOptimizer = AntColonyOptimizer(TSPAnt.__class__, 1, initializer, evaporator, intensifier, convergence_criterion)
antColonyOptimizer.optimize()