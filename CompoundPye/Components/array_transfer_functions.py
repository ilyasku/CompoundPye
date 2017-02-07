import numpy as np


def sigmoid(x, arg_array):
    return arg_array[:, 3] + arg_array[:, 2] / \
        (1 + np.exp(arg_array[:, 1] * (arg_array[:, 0] - x) + arg_array[:, 4]))


def linear(x, arg_array):
    return arg_array[:, 0] * x + arg_array[:, 1]


def identity(x, arg_array):
    """
    Linear function that can be used as a Component's transfer function.
    @return x*gain == input times gain
    """
    return x * arg_array[:, 0]


def quadratic(x, arg_array):
    """
    Quadratic function that can be used as a Component's transfer function.
    @return output of the quadratic function (a*x^2+b)
    """
    return arg_array[:, 0] * x**2 + arg_array[:, 1]


def power_law(x, arg_array):
    """
    Power law that can be used as a Component's transfer function.
    @return Output produced by the power law defined through b*x^a+c.
    """
    return arg_array[:, 1] * \
        (x + arg_array[:, 3]) ** arg_array[:, 0] + arg_array[:, 2]


assign_functions_dict = {'sigmoid': sigmoid, 'linear': linear,
                         'identity': identity, 'quadratic': quadratic,
                         'power_law': power_law}
