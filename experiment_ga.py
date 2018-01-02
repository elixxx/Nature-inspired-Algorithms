import random
from problems.makespan.makespan_candidate import Makespan as Makespan
import hippie.GA as GA
from experiment.generator import ExperimentGenerator
from experiment.worker import Worker
random.seed(3)

experiments_parms = {
    'n_generations': [100],
    'population_size':[100],
    'crossover': {'type': [GA.crossover.TwoPointCross, GA.crossover.OnePointCross],
                  'pb': [0.2, 0.5]},
    'mutation': {'type': [GA.mutation.CreepMutation],
                 'pb': [0.2],
                 'encoding_range': [Makespan.generate_random_candidate(conf="Bench1")._m]},
    'selection': [GA.selection.RouletteWheel(), {'type': [GA.selection.Tournament],
                                                         'tournement_size': [20,10],
                                                         'best_win_pb': [0.4]
                                                         }],
    'candidate_type': [Makespan],
    'candidate_gen_parms': {'type':[dict], 'conf': ["Bench1"]}
}
experiments = ExperimentGenerator(GA.Optimizer, experiments_parms, num_experiments=2)
arbeiter = Worker(experiments)
arbeiter.start()
arbeiter.wait()
# for i in experiments.experiment_instances():
#     # pprint(i)
#     opt = GA.Optimizer(**i)
#     # opt.optimize()
#     print("Done")