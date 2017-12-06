import pickle
from multiprocessing import Pool, Lock, Semaphore
import os, time, tqdm
from .generator import ExperimentGenerator


class Worker():
    """
    Execute Experiments of Experiment generator in a multiprocessed manner.
    Also only the num_worker_prcoess * 2 will be instanstiate to save memmory
    """
    def __init__(self, generator: ExperimentGenerator,
                 num_worker=None,
                 experiment_id=None,
                 path_log="log/"):
        """
        Create a Worker
        :param generator: ExperimentGenerator object
        :param num_worker: number of worker prcoesses: default len(os.sched_getaffinity(0)
        :param experiment_id: id of the Experiment, used for file saving: default time.time()
        :param path_log: path for saving the pickled results of Optimizer.optimize() default: log/
        """
        if num_worker is None:
            num_worker = len(os.sched_getaffinity(0))
        if experiment_id is None:
            experiment_id = time.time()

        self._log_path = path_log
        os.makedirs(path_log, exist_ok=True)
        self._experiment_id = experiment_id
        self._generator_object = generator

        self._pool = Pool(num_worker)
        self._semaphore = Semaphore(2 * num_worker)
        self._lock = Lock()

        self._finished = 0
        self._log_idx = -1
        self._tqdm = None

    def start(self, start_idx=0, stop_idx=-1):
        """
        Execute all Experiments between start_idx and stop_idx, by default anyone is executed.
        Function will return after any experiment is submited, this is not immediately and also not after all executions.
        Pls use Worker.wait() before the end of your programm!
        :param start_idx: start index for execution
        :param stop_idx: stop index for execution
        :return:
        """
        if stop_idx == -1:
            stop_idx = len(self._generator_object)
        self._log_idx = start_idx
        self._tqdm = tqdm.tqdm(total=stop_idx-start_idx)
        for i, experiment in enumerate(self._generator_object.experiment_instances()):
            if start_idx <= i <= stop_idx:
                self._semaphore.acquire()
                opti = self._generator_object.experiment_class(**experiment)
                self._pool.apply_async(opti.optimize,callback=self._callback)

    def _callback(self, a):
        """
        Callback which is invoked after an Experiment is done
        :param a: result of the Experiment (return of Optimizer.optimze())
        :return:
        """
        self._lock.acquire()
        my_finish_id = self._log_idx
        self._log_idx += 1
        self._finished += 1
        self._lock.release()
        self._tqdm.update(1)
        pickle.dump(a,open(os.path.join(self._log_path,
                                        str(self._experiment_id) + "-" + str(my_finish_id) + ".pkl"),
                           "wb"))
        self._semaphore.release()

    def wait(self):
        """
        Should called before your process end zo ensure any open Process/Execution is ended.
        Block until Pool is finished!
        :return:
        """
        self._pool.close()
        self._pool.join()