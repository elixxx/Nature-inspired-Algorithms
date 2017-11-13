import GA
import random
import copy
from typing import List


class Makespan(GA.ICandidate):
    def __init__(self, m, jobTimes, solution=None):
        self._m = m
        self._jobTimes = jobTimes
        if solution is None:
            self._solution = [random.choice(list(range(self._m))) for i in self._jobTimes]
        else:
            self._solution = solution

    def __eq__(self, other):
        return type(self) == type(other) and self._solution == other._solution

    def diversity(self, other):
        divs = 0
        for i, him in zip(self._solution, other._solution):
            if i != him:
                divs += 1
        if divs == 0:
            return 0
        return divs/len(self._solution)

    @classmethod
    def generate_random_candidate(cls, conf):
        if(conf=="Bench1"):
            # 6000 for benchmark problem 1
            m = 20
            jobs = [random.randint(10,300) for i in range(200)]
            jobs += [random.randint(100,300) for i in range(100)]
            return cls(m,jobTimes=jobs)
        elif(conf=="Bench2"):
            # 8000 for benchmark problem 2.
            m = 20
            jobs = [random.randint(10,1000) for i in range(150)]
            jobs += [random.randint(400,700) for i in range(150)]
            return cls(m,jobTimes=jobs)
        elif(conf=="Bench3"):
            m = 50
            jobs = [50 for i in range(3)]
            jobs += [random.randint(100, 300) for i in range(51, 100)]
            jobs += [random.randint(100, 300) for i in range(51, 100)]
            return cls(m,jobTimes=jobs)
        elif(conf=="test"):
            m = 8
            jobs = [random.randint(1,100) for i in range(10)]
            return cls(m,jobs)
        else:
            print("Unkonw config use one of follwing: 'Bench1','Bench2','Bench3'")
            exit(1)



    @property
    def cost(self):
        if self._cost is not None:
            return self._cost
        cost = [0]*self._m
        for jobID, machine in enumerate(self._solution):
            cost[machine]+=self._jobTimes[jobID]
        self._cost = max(cost)
        return self._cost

    @property
    def solution(self):
        self._cost = None
        return self._solution

class randomMutation(GA.IMutation):


    def __init__(self, pb):
        super().__init__(pb)

    def call(self, candidate: Makespan):
        for i, prop in enumerate(candidate.solution):
            if random.random() < self._pb:
                candidate.solution[i] = random.choice(list(range(candidate._m)))

class onePointCross(GA.ICrossover):

    def __init__(self, pb):
        super().__init__(pb)

    def numParents(self):
        return 2

    def call(self, parents :List[GA.ICandidate]) -> List[GA.ICandidate]:
        if len(parents) != 2:
            print("onePointCross takes only 2 parents")
            raise ValueError
        if random.random() > self._pb:
            return parents
        sol_length = len(parents[0].solution)
        cut = random.randint(1,sol_length)
        tmp = parents[0].solution[0:cut]
        parents[0].solution[0:cut] = parents[1].solution[0:cut]
        parents[1].solution[0:cut] = tmp
        return parents