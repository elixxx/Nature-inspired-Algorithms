from problems.differential_evolution.de_candidate import Profitmodel
from problems.differential_evolution.de_market import *
from problems.differential_evolution.de_plant import *

plant1 = PlantType(kwh_per_plant=50000, cost_per_plant=10000, max_number_of_plants=100)
plant2 = PlantType(kwh_per_plant=600000, cost_per_plant=80000, max_number_of_plants=50)
market1 = MarketType(max_price=0.45, max_demand=2000000)
market2 = MarketType(max_price=0.25, max_demand=30000000)

candidate1 = Profitmodel([plant1, plant2], [market1, market2])

print(candidate1.get_profit([10000, 1200000], [10000, 10000], [0.3, 0.2]))
candidate1.set_vector([0, 3000000, 0, 3000000, 0.3, 0.2])
print(candidate1)
print(candidate1.profit)


new_cand = Profitmodel.generate_random_candidate(plants = [plant1, plant2], markets = [market1, market2])
print(new_cand)
print(new_cand.profit)