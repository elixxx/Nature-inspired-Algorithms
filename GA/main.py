import random
import GA
import pandas as pd
random.seed(3)

# encapsulate GA
# Generate pd for log daten : fit of each candidate in population,
# Make sweet plots

mut = GA.randomMutation()
cross = GA.onePointCross()
sel = GA.RouletWheel()

pop = GA.Population(10,
                    crossover=cross,
                    mutation=mut,
                    selection=sel,
                    fnc_candidate_generator=lambda : GA.Makespan.generate_random_candidate(conf="test"))
for i in pop._population:
    print(i.cost)
pop.crossover(0.4)
pop.mutate(0.9)
pop.select()