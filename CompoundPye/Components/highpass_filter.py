## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 09.10.14

"""
@package CompoundPye.src.Components.highpass_filter
Holds the class HighpassFilter, which is a Component with a predefined
transfer function to turn it into a high-pass filter.

@todo I'm not happy with the high-pass filter's dependency on the time-step
dt! Need to change this! Same for the low pass.
"""

from .component import Component
from .component import identity


class HighpassFilter(Component):
    """
Component with a predefined transfer function turning it into a
high-pass filter.

It's probably better if time_const_output is of the same order as dt.

@todo Investigate the influence of time_const_output. Should I rather set it
to dt, such that dt/time_const=1?
    """

    def __init__(self, time_const_RC, time_const_output, debug=False):
        """
Initializes a HighpassFilter object.
@param time_const_RC Time constant as in an electrical high-pass filter.
@param dt Based on wikipedia's description of a high-pass filter, the time-step
dt is required for the transfer function.
@param debug Set False, if you don't want to see debugging output, set True
if you want to see debugging output.
        """
        Component.__init__(self, identity, [1.0], 0, time_const_output, debug)
        self.time_const_RC = time_const_RC

        # In addition to a normal Component's variables, a HighpassFilter
        # requires the previous input value for an update.
        self.input_pre = 0

    def update(self, input, dt):
        """
Updates the Component.
Similar to Component.update, but it additionally requires to store the
current value in HighpassFilter.input_pre.
        """
        beta = self.time_const_RC / (self.time_const_RC + dt)

        self.value = beta * (input - self.input_pre + self.value)
        self.output += dt / self.time_const_output * \
                       (-self.output + self.activation_func(self.value, *self.param))

        self.input_pre = input


class HighpassFilter2(HighpassFilter):
    """
    Similar to HighpassFilter. See also Component2.
    """
    def __init__(self, transfer_func, transfer_func_params, time_const_RC,
                 time_const_output, debug=False):
        Component.__init__(self, transfer_func, transfer_func_params,
                           0, time_const_output, debug)

        self.time_const_RC = time_const_RC
        self.input_pre = 0

