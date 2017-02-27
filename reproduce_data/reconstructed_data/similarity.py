"""
To optimize my Tm3 and Mi1 I need to match my output with Behnia's recordings
as good as possible. For that I want to define a similarity value comparing
two graphs.
"""
import numpy as np


def similarity(x, y):
    sim = np.corrcoef(x, y)
    return sim[0, 1]


def similarity_z(x, y):
    x_z = (x - x.mean()) / x.std()
    y_z = (y - y.mean()) / y.std()

    sim = np.corrcoef(x_z, y_z)
    return sim[0, 1], x_z, y_z
