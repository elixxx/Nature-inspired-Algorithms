from hippie.GA.base import *
import random
import numpy as np
from typing import List


class Makespan(BaseGACandidate):
    def __init__(self, m, jobTimes, solution=None):
        self._m = m
        self._jobTimes = jobTimes
        self._cost = None
        if solution is None:
            # self._solution = np.array([random.choice(list(range(self._m))) for i in self._jobTimes])
            self._solution = np.random.choice(self._m, size=len(self._jobTimes), replace=True)
        else:
            self._solution = solution



    def __str__(self):
        return "GACandidate.Makespane"

    def diversity(self, other):
        return 1
        divs = 0
        for i, him in zip(self._solution, other._solution):
            if i != him:
                divs += 1
        if divs == 0:
            return 0
        return divs/len(self._solution)

    @classmethod
    def generate_random_candidate(cls, conf):
        if(conf == "Bench1"):
            # 6000 for benchmark problem 1
            m = 20
            jobs = [random.randint(10,1000) for i in range(200)]
            jobs += [random.randint(100,300) for i in range(100)]
            return cls(m,jobTimes=np.array(jobs))
        elif(conf=="Bench2"):
            # 8000 for benchmark problem 2.
            m = 20
            jobs = [random.randint(10,1000) for i in range(150)]
            jobs += [random.randint(400,700) for i in range(150)]
            return cls(m, jobTimes=np.array(jobs))
        elif(conf=="Bench3"):
            m = 50
            jobs = [50 for i in range(3)]
            jobs += [i for i in range(51, 100)]
            jobs += [i for i in range(51, 100)]
            return cls(m, jobTimes=np.array(jobs))
        elif(conf=="test"):
            m = 8
            jobs = [random.randint(1,100) for i in range(10)]
            return cls(m, jobTimes=np.array(jobs))
        else:
            print("Unkonw config use one of follwing: 'Bench1','Bench2','Bench3'")
            exit(1)

    @property
    def cost(self):
        if self._cost is not None:
            return self._cost
        cost = [0] * self._m
        for jobID, machine in enumerate(self._solution):
            cost[machine] += self._jobTimes[jobID]
        self._cost = max(cost)
        return self._cost

    @property
    def solution(self):
        self._cost = None
        return self._solution

    def __getitem__(self, item):
        self._cost = None
        return self._solution[item]

    def __setitem__(self, key, value):
        self._solution[key] = value

    def __len__(self):
        return len(self._solution)


