import random
import time
import tqdm
import copy
from hippie.differential_evolution.optimizer import DifferentialEvolutionOptimizer
from hippie.differential_evolution.differential_mutation import DifferentialMutation
from hippie.differential_evolution.crossover import Crossover
from hippie.differential_evolution.selection import Selection
from hippie.differential_evolution.convergence import MaxIteration
from problems.differential_evolution.problem import Problem
from problems.differential_evolution.de_market import MarketType
from problems.differential_evolution.de_plant import PlantType
from experiment.generator import ExperimentGenerator
from experiment.worker import Worker
# random.seed(3)

plant1 = PlantType(kwh_per_plant=50000, cost_per_plant=10000, max_number_of_plants=100)
plant2 = PlantType(kwh_per_plant=600000, cost_per_plant=80000, max_number_of_plants=50)
plant3 = PlantType(kwh_per_plant=4000000, cost_per_plant=400000, max_number_of_plants=3)
market1 = MarketType(max_price=0.45, max_demand=2000000)
market2 = MarketType(max_price=0.25, max_demand=30000000)
market3 = MarketType(max_price=0.2, max_demand=20000000)

n_pop = 100
n_experiments = 30
problem1 = Problem([plant1, plant2, plant3], [market1, market2, market3])

# for i in tqdm.tqdm(range(n_experiments)):
experiments_parms = {
        'population': {'type': [copy.deepcopy(problem1.generate_list_of_random_candidates)],
                       'number_of_candidates': [n_pop]
                       },
        'problem': [problem1],
        'crossover': {'type': [Crossover],
                      'crossover_rate': [0.6, 0.5, 0.7]
                      },
        'differential_mutation': {'type': [DifferentialMutation],
                                  'scaling_factor': [0.6, 0.5, 0.7]
                                  },
        'selection': [Selection()],
        'convergence_criterion': {'type': [MaxIteration], 'n_max_iterations': [1200]},
    }
experiments = ExperimentGenerator(DifferentialEvolutionOptimizer, experiments_parms)
arbeiter = Worker(experiments)
arbeiter.start()
arbeiter.wait()