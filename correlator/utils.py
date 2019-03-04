from contextlib import contextmanager
from multiprocessing import Pool

import numpy as np


def distance(instance1, instance2):
    # just in case, if the instances are lists or tuples:
    instance1 = np.array(instance1)
    instance2 = np.array(instance2)
    error = np.square(instance1 - instance2)
    return np.sqrt(np.sum(error))


def get_neighbors(test_instance, training_set, distance=distance):
    """
    get_neighors calculates a list of the k nearest neighbors
    of an instance 'test_instance'.
    The list neighbors contains 3-tuples with  
    (index, dist, label)
    where 
    index    is the index from the training_set, 
    dist     is the distance between the test_instance and the 
             instance training_set[index]
    distance is a reference to a function used to calculate the 
             distances
    """
    k = 1
    distances = []
    for index in range(len(training_set)):
        dist = distance(test_instance, training_set[index, 1:])
        distances.append((training_set[index], dist))
    distances.sort(key=lambda x: x[1])
    neighbors = distances[:k]
    return neighbors


@contextmanager
def poolcontext(*args, **kwargs):
    pool = Pool(*args, **kwargs)
    yield pool
    pool.terminate()
