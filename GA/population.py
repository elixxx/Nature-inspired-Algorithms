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
        # self._candidate_generator = fnc_candidate_generator
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
                steps += 1
        self._diversity = cum_div/steps
        return self._diversity

    def mutate(self):
        self._diversity = None
        for i, cand in enumerate(self._population):
            self._mutation.call(self._population[i])

    def crossover(self):
        self._diversity = None
        for i, cand in enumerate(self._population):
            for a in range(i,self._size):
                self._crossover.call((self._population[i],self._population[a]))

    def select(self):
        self._diversity = None
        self._population = self._selection.select(self._population)

    def gatherPandas(self):
        pd = pandas.DataFrame(columns=["CrossOP","CrossPB","MutOP","MutPB", "SelectionOP", "FitMin", "Div"])
        pd["CrossOP"] = self._crossover
        pd.loc[0] = [str(type(self._crossover)),
                     self._crossover.pb,
                     str(type(self._mutation)),
                     self._mutation.pb,
                     str(type(self._selection)),
                     max([ind.cost for ind in self._population]),
                     self.diversity]
        return pd
