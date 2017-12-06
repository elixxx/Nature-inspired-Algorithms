from problems.travelling_salesman.tsp_candidate import *
from problems.travelling_salesman.parser import *
from experiment.generator import ExperimentGenerator
from experiment.worker import Worker
from hippie.ant_colony.initializer import *
from hippie.ant_colony.evaporator import *
from hippie.ant_colony.intensifier import *
from hippie.ant_colony.optimizer import *
from hippie.ant_colony.convergence import *

problem = "1.tsp"
distance_matrix = parse_to_matrix("problems/travelling_salesman/data/"+problem)

experiments_parms = {
    'n_ants': [10],
    'initializer': [ConstantInitializer(distance_matrix.shape[0], 1)],
    'evaporator': {'type': [Evaporator], 'rate': [0.1]},
    'intensifier': {'type': [BestIntensifier], 'pheromone_increase': [0.5, 5]},
    'convergence_criterion': {'type': [MaxIteration], 'n_max_iterations': [120]},
    'ant_type': [LogicalTSPAnt],
    'ant_gen_parms': {'type':[dict],
                      'distance_matrix': [distance_matrix],
                      'pathfinding_alpha': [1],
                      'pathfinding_beta': [0]}


}
experiments = ExperimentGenerator(AntColonyOptimizer, experiments_parms)
arbeiter = Worker(experiments)
arbeiter.start()
arbeiter.wait()