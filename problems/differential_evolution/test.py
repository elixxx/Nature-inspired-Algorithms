from problems.differential_evolution.de_candidate import *
from problems.differential_evolution.problem import *
from problems.differential_evolution.de_market import *
from problems.differential_evolution.de_plant import *

plant1 = PlantType(kwh_per_plant=50000, cost_per_plant=10000, max_number_of_plants=100)
plant2 = PlantType(kwh_per_plant=600000, cost_per_plant=80000, max_number_of_plants=50)
market1 = MarketType(max_price=0.45, max_demand=2000000)
market2 = MarketType(max_price=0.25, max_demand=30000000)

problem = Problem([plant1, plant2], [market1, market2])
candidate = problem.generate_random_candidate()

print(candidate.get_profit([10000, 1200000], [10000, 10000], [0.3, 0.2]))
candidate.set_vector([0, 3000000, 0, 3000000, 0.3, 0.2])
print(candidate)
print(candidate.profit)


new_cand = problem.generate_random_candidate()
print(new_cand)
print(new_cand.profit)