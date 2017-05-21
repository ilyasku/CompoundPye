## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 09.10.14

"""
@package CompoundPye.src.Components.lowpass_filter
Holds the class LinearInputFilter, a Component with a predefined transfer
function turning it into a low-pass filter.

@todo Somehow get rid of the dependency on dt.
"""

from .component import Component
from .component import identity


class LowpassFilter(Component):
    """
LowpassFilter is a Component with a predefined transfer function, turning it
into a low-pass filter.
    """
    def __init__(self, time_const_RC, time_const_output, debug=False):
        """
        Initializes a LowpassFilter-object.
        @param time_const_RC Time constant as in a electrical low-pass filter.
        @param dt Based on wikipedia's description of a low-pass filter, the
        time-step dt is required for the transfer function.
        """
        Component.__init__(self, identity, [], 0, time_const_output, debug)
        self.time_const_RC = time_const_RC

    def update(self, input, dt):
        alpha = dt / (self.time_const_RC + dt)
        self.value += alpha * (-self.value + input)
        self.output += dt / self.time_const_output * (-self.output + self.activation_func(self.value, *self.param))


class LowpassFilter2(LowpassFilter):
    """
    Similar to LowpassFilter. See also Component2.
    """
    def __init__(self, transfer_function, transfer_func_params,
                 time_const_RC, time_const_output, debug=False):
        Component.__init__(self, transfer_function,
                           transfer_func_params, 0, time_const_output, debug)
        self.time_const_RC = time_const_RC
