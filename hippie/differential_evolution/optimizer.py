import hippie.interfaces as interfaces
import numpy as np


class DifferentialEvolutionOptimizer(interfaces.BaseOptimizer):

    def __init__(self, population, differential_mutation, crossover, selection, problem, convergence_criterion ):
        self._population = population
        self._convergence_criterion = convergence_criterion
        self._differential_mutation = differential_mutation
        self._crossover = crossover
        self._selection = selection
        self._problem = problem

    def optimize(self):

        while not self._convergence_criterion.converged(self):

            trial_candidates = []
            for target in self._population:
                donor_vector = self._differential_mutation.mutate(target, self._population)
                trial_vector = self._crossover.crossover(target.vector, donor_vector)
                trial_candidates.append(self._problem.generate_candidate(vector=trial_vector))

            self._population = self._selection.select(self._population, trial_candidates)

            print(f'Max Profit of Iteration is {max([current_candidate.profit for current_candidate in self._population ])}')

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


