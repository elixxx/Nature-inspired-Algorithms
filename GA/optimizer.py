import GA
from tqdm import tqdm
import pandas as pd
class Optimizer:

    def __init__(self, n_generations, population_size, crossover, mutation, selection, fnc_candidate_generator):
        self._population = GA.Population(population_size,
                                         crossover=crossover,
                                         mutation=mutation,
                                         selection=selection,
                                         fnc_candidate_generator=fnc_candidate_generator)
        self._n_generations = n_generations

    def optimize(self):

        generations_without_improvment = 0
        last_min_fitness = float("inf")
        last_frame = None
        n_generation = 0
        # for i in range(generations):
        while generations_without_improvment < 10:
            self._population.crossover()
            self._population.mutate()
            self._population.select()
            frame = self._population.gatherPandas()
            if last_min_fitness < frame["FitMin"][0]:
                generations_without_improvment +=1
            else:
                generations_without_improvment = 0
                last_min_fitness = frame["FitMin"][0]
                last_frame = frame
            if n_generation >self._n_generations:
                return last_frame

            # results = results.append(frame, ignore_index=True)
        return last_frame
