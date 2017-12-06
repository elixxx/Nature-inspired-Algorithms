import pandas as pd
from multiprocessing import Pool, Lock
import os, time, tqdm
from .generator import ExperimentGenerator

class Worker():
    def __init__(self, generator :ExperimentGenerator, num_worker=None, experiment_id = None ):
        if num_worker is None:
            num_worker = len(os.sched_getaffinity(0))
        if experiment_id is None:
            experiment_id = time.time()

        self._experiment_id = experiment_id
        self._generator_object = generator
        self._pool = Pool(num_worker)
        self._finished = 0
        self._to_work_on = -1
        self._tqdm = None
        self._lock = Lock()

    def start(self, start_idx=0, stop_idx=-1):
        if stop_idx == -1:
            stop_idx = len(self._generator_object)
        self._tqdm = tqdm.tqdm(total=stop_idx-start_idx)
        for i, experiment in enumerate(self._generator_object.experiment_instances()):
            if start_idx <= i <=stop_idx:
                opti = self._generator_object.experiment_class(**experiment)
                self._results = self._pool.apply_async(opti.optimize,callback=self.callback)

    def callback(self, a):
        self._lock.acquire()
        my_finischid = self._finished
        self._finished += 1
        self._lock.release()
        self._tqdm.update(1)
        frame = pd.DataFrame(a)
        frame.to_pickle(str(self._experiment_id) + "-" + str(my_finischid) + ".pkl")

    def wait(self):
        self._pool.close()
        self._pool.join()