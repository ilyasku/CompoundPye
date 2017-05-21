## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 14.11.14

"""
@package CompoundPye.src.Sensors.dummy_sensor

Provides the DummySensor class, which is actually a Sensor-object that does
nothing. It can be used to pass values to Components, though, if one wants to
skip the Stimulus and Sensor steps and directly provide values to the circuit
of Components.
"""

from . import sensor


class DummySensor(sensor.Sensor):

    def __init__(self):
        sensor.Sensor.__init__(self)

    def update(self, single_value):
        self.value = single_value
