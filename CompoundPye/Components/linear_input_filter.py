## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 09.10.14

"""
@package CompoundPye.src.Components.linear_input_filter
Holds the class LinearInputFilter, a Component with a predefined
linear transfer function.

@todo  cover exception in receptive field values (see note)
@todo cover more than one-dimensional case! (in set_norm_factor())
"""

import numpy as np
from . import component


class LinearInputFilter(component.Component):
    """
LinearInputFilter is a Component with a predefined linear transfer function.
One can use the function LinearInputFilter.set_norm_factor to normalize the
Component's output based on a sensors' input.
    """
    def __init__(self, time_const_input=0.05, time_const_output=0.05,
                 debug=False):
        """
        Initializes  LinearInputFilter-object.
        @param time_const The Component's time constant, which specifies how
        much of its previous value remains after each update step.
        @param debug Set False, if you don't want to see debugging output,
        set True if you want to see debugging output.
        """
        component.Component.__init__(self, component.identity, [],
                                     time_const_input, time_const_output,
                                     debug)

    def set_norm_factor(self, surrounding_area, sensor_receptive_field):
        """
        Sets the normalization factor of the LinearInputFilter, depending on
        the area that is covered by the sensor connected to the input filter.
        @param surrounding_area Area of the complete surrounding (of the
        MotionDetectorModel.Surroundings.surrounding.Surrounding object).
        @param sensor_receptive_field Receptive field of the sensor, usually
        given in a list of min and max angles.
        """
        if len(sensor_receptive_field) == 1:
            ## @note what happens if receptive field min> receptive field max?
            self.param = [1./(surrounding_area
                              * (sensor_receptive_field[0][1]
                                 - sensor_receptive_field[0][0])/2./np.pi)]
        else:
            raise NotImplementedError("Not implemented yet!")

