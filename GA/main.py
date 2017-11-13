import random
import GA
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt

pd.set_option('display.expand_frame_repr', False)
random.seed(3)

# encapsulate GA
# Generate pd for log daten : fit of each candidate in population,
# Make sweet plots

mut = GA.randomMutation(0.08)
cross = GA.onePointCross(0.8)
sel = GA.RouletWheel()
generations = 20
pop = GA.Population(300,
                    crossover=cross,
                    mutation=mut,
                    selection=sel,
                    fnc_candidate_generator=lambda: GA.Makespan.generate_random_candidate(conf="Bench1"))
results = pd.DataFrame()


for i in tqdm(range(generations)):

    pop.crossover()
    pop.mutate()
    pop.select()
    tmp = pop.gatherPandas()
    results = results.append(tmp,ignore_index=True)
print(results)
results.plot(y=["FitBEST","FitAVG"])
results.plot(y="Div")
plt.show()