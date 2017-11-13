from GA import ICandidate, ICrossover, IMutation, ISelection
import pandas
class Population():
    def __init__(self, size: int,
                 mutation: IMutation,
                 crossover: ICrossover,
                 selection: ISelection,
                 fnc_candidate_generator):
        self._size = size
        self._mutation = mutation
        self._crossover = crossover
        self._selection = selection
        self._candidate_generator = fnc_candidate_generator
        self._population = [fnc_candidate_generator() for i in range(size)]
        self._diversity = None

    @property
    def diversity(self):
        if self._diversity is not None:
            return self._diversity
        steps = 0
        cum_div = 0
        for i, cand in enumerate(self._population):
            for a in range(i,self._size):
                cum_div += cand.diversity(self._population[a])
        self._diversity = cum_div/steps
        return self._diversity

    def mutate(self, pb):
        self._diversity = None
        for i, cand in enumerate(self._population):
            self._population[i] = self._mutation.call(self._population[i], pb)

    def crossover(self, pb):
        self._diversity = None
        for i, cand in enumerate(self._population):
            for a in range(i,self._size):
                self._population[i], self._population[a] = self._crossover.call((self._population[i],self._population[a]),pb)

    def select(self):
        self._diversity = None
        self._population = self._selection.select(self._population)

    def gatherPandas(self):
        pd = pandas.DataFrame()