
from hippie.differential_evolution.optimizer import *
from hippie.differential_evolution.convergence import *
from hippie.differential_evolution.crossover import *
from hippie.differential_evolution.differential_mutation import *
from hippie.differential_evolution.selection import *
from problems.differential_evolution.de_candidate import *
from problems.differential_evolution.de_market import *
from problems.differential_evolution.de_plant import *
from problems.differential_evolution.problem import *
import pickle

population_size = 100
number_of_iterations = 3000
crossover_rate = 0.6
scaling_factor = 0.3        # 0.6; 0.3; 0.1

convergence = MaxIteration(number_of_iterations)
crossover = Crossover(crossover_rate)
differential_mutation = DifferentialMutation(scaling_factor)
selection = Selection()

plant1 = PlantType(kwh_per_plant=50000, cost_per_plant=10000, max_number_of_plants=100)
plant2 = PlantType(kwh_per_plant=600000, cost_per_plant=80000, max_number_of_plants=50)
plant3 = PlantType(kwh_per_plant=4000000, cost_per_plant=400000, max_number_of_plants=3)

market1 = MarketType(max_price=0.45, max_demand=2000000)
market2 = MarketType(max_price=0.25, max_demand=30000000)
market3 = MarketType(max_price=0.2, max_demand=20000000)

market4 = MarketType(max_price=0.5, max_demand=1_000_000)
market5 = MarketType(max_price=0.3, max_demand=5_000_000)
market6 = MarketType(max_price=0.1, max_demand=5_000_000)

problem1 = Problem([plant1, plant2, plant3], [market1, market2, market3])
problem2 = Problem([plant1, plant2, plant3], [market1, market2, market3], energy_purchasing_price=0.1)
problem3 = Problem([plant1, plant2, plant3], [market4, market5, market6], energy_purchasing_price=0.6)


problem = problem1

population = problem.generate_list_of_random_candidates(population_size)

optimizer = DifferentialEvolutionOptimizer(population=population,
                                           problem=problem,
                                           convergence_criterion=convergence,
                                           crossover=crossover,
                                           selection=selection,
                                           differential_mutation=differential_mutation)
_ = optimizer.optimize()

pickle.dump(optimizer,
            open('problem1.pkl',
                 'wb'))