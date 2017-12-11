import random
from hippie.differential_evolution.optimizer import DifferentialEvolutionOptimizer
from hippie.differential_evolution.differential_mutation import DifferentialMutation
from hippie.differential_evolution.crossover import Crossover
from hippie.differential_evolution.selection import Selection
from hippie.differential_evolution.convergence import MaxIteration
from problems.differential_evolution.de_candidate import Profitmodel
from problems.differential_evolution.de_market import *
from problems.differential_evolution.de_plant import *
from experiment.generator import ExperimentGenerator
from experiment.worker import Worker
random.seed(3)

plant1 = PlantType(kwh_per_plant=50000, cost_per_plant=10000, max_number_of_plants=100)
plant2 = PlantType(kwh_per_plant=600000, cost_per_plant=80000, max_number_of_plants=50)
plant3 = PlantType(kwh_per_plant=4000000, cost_per_plant=400000, max_number_of_plants=3)
market1 = MarketType(max_price=0.45, max_demand=2000000)
market2 = MarketType(max_price=0.25, max_demand=30000000)
market3 = MarketType(max_price=0.2, max_demand=20000000)
n_pop = 10
# plants, markets,
de = DifferentialEvolutionOptimizer([Profitmodel.generate_random_candidate(plants = [plant1, plant2, plant3],
                                                                           markets = [market1, market2, market3])
                                     for i in range(n_pop) ],
                                    DifferentialMutation(scaling_factor=0.5),
                                    Crossover(crossover_rate=0.2),
                                    Selection(),
                                    Profitmodel(plants=[plant1,plant2],markets=[market1,market2]),
                                    convergence_criterion=MaxIteration(10))
de.optimize()
# experiments_parms = {
#     'population':[100],
#     'crossover': {'type': [Crossover],
#                   'pb': [0.2, 0.5]},
#     'differential_mutation': {'type': [DifferentialMutation],
#                  'scaling_factor': [0.5]},
#     'selection': [Selection],
#     'convergence_criterion': {'type':[MaxIteration], 'n_max_iterations': [10]},
#     'candidate': {'type': [Profitmodel],
#                   'plants':{'type': list}},
# }
# experiments = ExperimentGenerator(DifferentialEvolutionOptimizer, experiments_parms)
# arbeiter = Worker(experiments)
# arbeiter.start()
# arbeiter.wait()
# for i in experiments.experiment_instances():
#     # pprint(i)
#     opt = GA.Optimizer(**i)
#     # opt.optimize()
#     print("Done")