## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 14.11.14
# last update: 01.10.2015

"""
@package CompoundPye.src.Components.transfer_functions
Provides some transfer functions.

@todo build a sigmoid wrapper function? so that one can combine any function f(x) with an sigmoidal output s(f(x)). 
"""

import numpy as np

def sigmoid(x,threshold,alpha,c=1.,offset=0.0,exp_offset=0):
    return offset+c/(1+np.exp(alpha*(threshold-x)+exp_offset))

def linear(x,a=1,b=0):
    return a*x+b

def identity(x,gain=1.0):
    """
    Linear function that can be used as a Component's transfer function.
    @return x*gain == input times gain
    """
    return x*gain


def quadratic(x,a=1,b=0):
    """
    Quadratic function that can be used as a Component's transfer function.
    @return output of the quadratic function (a*x^2+b)
    """
    return a*x**2+b



def power_law(x,a,b=1,c=0,d=0):
    """
    Power law that can be used as a Component's transfer function.
    @return Output produced by the power law defined through b*x^a+c.
    """
    return b*(x+d)**a+c
