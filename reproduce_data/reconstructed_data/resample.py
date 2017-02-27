"""
In order to filter the plot digitized data or to calculate similarity with my model's data, 
I want to resample/stretch them to be evenly spaced in time.
"""
import numpy as np


def resample(x, old_t, new_t):
    new_x = np.ones_like(new_t) * x[0]
    for i in range(1, old_t.shape[0]):
        new_t_indices = np.where((new_t >= old_t[i - 1]) & (new_t < old_t[i]))[0]
        new_x[new_t_indices] = np.linspace(x[i - 1], x[i], len(new_t_indices))
    return new_x
