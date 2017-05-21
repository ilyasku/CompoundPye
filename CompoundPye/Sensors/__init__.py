## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 09.10.14

"""
@package CompoundPye.src.Sensors
Provides Sensor classes.

Sensors contain information about 'what they see' in the System's Surroundings.
They have connections to Components to pass their sensory information
to a network of Components.
Usually you should provide the Sensor's output to an input filter, which has
the job to somehow normalize the Sensor's output. A tool for normalization is
not provided in the Sensor unit itself yet.
"""

from . import sensor
from . import dummy_sensor

from . import photoreceptor
