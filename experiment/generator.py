from copy import deepcopy
import hippie.interfaces as interfaces
import collections

class ExperimentGenerator:
    """
    Generate experiments given a optimizer class and a dict containing the required values und Strategys as a dict of type:
    experiments_parms = {
    'n_generations': [100],
    'population_size':[100],
    'crossover': {'type': [GA.crossover.TwoPointCross, GA.crossover.OnePointCross],
                  'pb': [0.2, 0.5]},
    'mutation': {'type': [GA.mutation.CreepMutation],
                 'pb': [0.2],
                 'encoding_range': [Makespan.generate_random_candidate("Bench1")._m]},
    'selection': [GA.selection.RouletteWheel(), {'type': [GA.selection.Tournament],
                                                         'tournement_size': [20],
                                                         'best_win_pb': [0.4]
                                                         }],
    'candidate_type': [Makespan],
    'candidate_gen_parms': ["Bench1"]
}
    """
    def __init__(self, optimizer_type: interfaces.BaseOptimizer, experiment_dict: dict):
        """

        :param self:
        :param optimizer_type: Optimizer for which the experiments willbe created
        :param experiment_dict: dict which have a list for each parameter of optimizer_type with len() bigger 1
        :return:
        """
        self._optimizer_type = optimizer_type
        self._experiment_dict = experiment_dict
        self._experiments = list(self._recursive_recombine(not_parse=self._experiment_dict))

    def _recursive_recombine(self,not_parse, partial_experiment=None):
        if len(not_parse) == 0:
            # print(partial_experiment)
            yield partial_experiment
            return
        if partial_experiment is None:
            partial_experiment = {}

        name = list(not_parse.keys())[0]
        entry = not_parse.pop(name)
        if isinstance(entry,dict):
            ops = self._recursive_recombine(entry.copy())
            for op in ops:
                sub_partial_experiment = partial_experiment.copy()
                sub_partial_experiment[name] = op
                yield from self._recursive_recombine(not_parse.copy(), sub_partial_experiment)
        elif isinstance(entry,collections.Iterable):
            for e in entry:
                if isinstance(e, dict):
                    ops = self._recursive_recombine(e.copy())
                    for op in ops:
                        sub_partial_experiment = partial_experiment.copy()
                        sub_partial_experiment[name] = op
                        yield from self._recursive_recombine(not_parse.copy(), sub_partial_experiment)
                else:
                    sub_partial_experiment = partial_experiment.copy()
                    sub_partial_experiment[name] = e
                    yield from self._recursive_recombine(not_parse.copy(), sub_partial_experiment)
        else:
            print("Entry have to be dict or iterable!")
            print(entry)
            raise ValueError

    def __len__(self):
        return len(self._experiments)

    def experiment_instances(self):
        """
        Generater function to get a instance of each Experiment. Parameter class are created jsut in time to save memory
        :return: generator to a optimizer instance
        """
        for experiment in self._experiments.copy():
            # print(experiment)
            to_yield = {}
            for key, value in deepcopy(experiment).items():
                if isinstance(value, dict):
                    parm_type = value.pop('type')
                    to_yield[key] = parm_type(**value)
                else:
                    to_yield[key] = value
            yield to_yield

    @property
    def experiment_class(self)-> interfaces.BaseOptimizer:
        return self._optimizer_type