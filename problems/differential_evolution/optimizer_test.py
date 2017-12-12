
from hippie.differential_evolution.optimizer import *
from hippie.differential_evolution.convergence import *
from hippie.differential_evolution.crossover import *
from hippie.differential_evolution.differential_mutation import *
from hippie.differential_evolution.selection import *
from problems.differential_evolution.de_candidate import *
from problems.differential_evolution.de_market import *
from problems.differential_evolution.de_plant import *


population_size = 100
number_of_iterations = 400
crossover_rate = 0.6
scaling_factor = 3

convergence = MaxIteration(number_of_iterations)
crossover = Crossover(crossover_rate)
differential_mutation = DifferentialMutation(scaling_factor)
selection = Selection()

plant1 = PlantType(kwh_per_plant=50000, cost_per_plant=10000, max_number_of_plants=100)
plant2 = PlantType(kwh_per_plant=600000, cost_per_plant=80000, max_number_of_plants=50)
market1 = MarketType(max_price=0.45, max_demand=2000000)
market2 = MarketType(max_price=0.25, max_demand=30000000)

profitmodel = Profitmodel([plant1, plant2], [market1, market2])

population = [Profitmodel.generate_random_candidate(plants = [plant1, plant2], markets = [market1, market2])
                                for _ in range(population_size)]

optimizer = DifferentialEvolutionOptimizer(population=population, candidate=profitmodel, convergence_criterion=convergence,
                                           crossover=crossover,
                                           selection=selection, differential_mutation=differential_mutation)

sth = optimizer.optimize()
