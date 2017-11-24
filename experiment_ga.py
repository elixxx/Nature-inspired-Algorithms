import time
from multiprocessing import Pool
import pandas as pd
from tqdm import tqdm
import random
import multiprocessing
import itertools
from problems.makespan.makespan import Makespan as Makespan
import hippie.GA as GA

pd.set_option('display.expand_frame_repr', False)
random.seed(3)

# problem in pandas

def experiment(generations, mut_rates, mut_classes, cross_rates, cross_classes, pop_sizes, sel_instances, benchmarks):
    number = (len(mut_rates) * len(mut_classes) * len(cross_rates)
             * len(cross_classes) * len(pop_sizes)
             * len(sel_instances) * len(benchmarks))
    print("Num of experiments: ", number)
    arbeiter_becken = Pool(multiprocessing.cpu_count())
    gas = list()
    optimized_fitnesses = list()
    for mut_class in mut_classes:
        for cross_class in cross_classes:
            for cross_instance in map(cross_class, cross_rates):
                for pop_size in pop_sizes:
                    for sel_instance in sel_instances:
                        for benchmark in benchmarks:
                            for mut_instance in map(mut_class, mut_rates, itertools.repeat(2, len(Makespan.generate_random_candidate(benchmark)))):
                                for run in range(2):
                                    gas.append(GA.Optimizer(n_generations=generations,
                                                            population_size=pop_size,
                                                            crossover=cross_instance,
                                                            mutation=mut_instance,
                                                            selection=sel_instance,
                                                            candidate_type=Makespan,
                                                            candidate_gen_parms=benchmark))
                                    optimized_fitnesses.append(arbeiter_becken.apply_async(gas[-1].optimize))
    frame = pd.DataFrame()
    for f in tqdm(optimized_fitnesses):
        frame = frame.append(f.get(), ignore_index=True)
    arbeiter_becken.close()
    arbeiter_becken.join()
    return frame

# Make sweet plots
mut_rates = [0.1]
mut_classes = [GA.mutation.RandomMutation, GA.mutation.CreepMutation]
cross_rates =[0.3]
cross_classes = [GA.crossover.OnePointCross, GA.crossover.TwoPointCross]
pop_sizes = [40]
benchmarks = ["Bench1"]
sel_instances = [GA.selection.Tournament(20, 0.75), GA.selection.RouletteWheel()]
#mut_rates = np.arange(0.35, 0.45, 0.1)
#mut_classes = [GA.RandomMutation,]
#cross_rates = np.arange(0.8, 0.9, 0.1)
#cross_classes = [GA.OnePointCross,GA.TwoPointCross]
#pop_sizes = np.arange(50, 100, 50)
#benchmarks = ["Bench1", "Bench2", "Bench3"]
#sel_instances = [GA.RouletteWheel(), GA.TournamentSelection(20, 0.75)]
generations = 1

results = experiment(generations, mut_rates, mut_classes, cross_rates, cross_classes, pop_sizes, sel_instances, benchmarks)
results.to_pickle(str(time.time())+"log.pkl")
print("Finished")

time.sleep(20)
