import hippie.interfaces as interfaces
import numpy as np


class DifferentialEvolutionOptimizer(interfaces.BaseOptimizer):

    def __init__(self, population, differential_mutation, crossover, selection, candidate, convergence_criterion ):
        self._population = population
        self._convergence_criterion = convergence_criterion
        self._differential_mutation = differential_mutation
        self._crossover = crossover
        self._selection = selection
        self._candidate = candidate

    def optimize(self):

        while not self._convergence_criterion.converged(self):

            trial_candidates = []
            for target in self._population:
                donor_vector = self._differential_mutation.mutate(target, self._population)
                trial_vector = self._crossover.crossover(target.vector, donor_vector)
                trial_candidates.append(self._candidate.generate_candidate(vector=trial_vector, plants=target._plants,
                                                                           markets=target._markets))

            self._population = self._selection.select(self._population, trial_candidates)

        return self

    def __str__(self):
        return f'Optimizer with {len(self._population)} vectors.'

    @property
    def parameters(self):
        return {'population size': len(self._population),
                'differential mutation': self._differential_mutation.parameters,
                'crossover': self._crossover.parameters,
                'selection': self._selection.paramaters,
                'convergence_criterion': self._convergence_criterion.parameters}


