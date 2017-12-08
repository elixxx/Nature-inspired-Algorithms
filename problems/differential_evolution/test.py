from problems.differential_evolution.de_candidate import *
from problems.differential_evolution.de_market import *
from problems.differential_evolution.de_plant import *

plant1 = PlantType(kwh_per_plant=50000, cost_per_plant=10000, max_number_of_plants=100)
market1 = MarketType(max_price=0.45, max_demand=2000000)
candidate1 = Profitmodel([plant1], [market1])

print(candidate1.profit([10000], [10000], [0.3]))