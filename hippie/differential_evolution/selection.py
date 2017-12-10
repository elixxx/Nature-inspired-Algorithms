import hippie.interfaces as interfaces


class Selection(interfaces.BaseStrategy):

    def select(self, population, trial_candidates):

        new_population = []

        for target, trial in zip(population, trial_candidates):
            if target.profit >= trial.profit:
                new_population.append(target)
            else:
                new_population.append(trial)

        return new_population

    @property
    def parameters(self):
        return {}

    def __str__(self):
        return 'No attributes available'
