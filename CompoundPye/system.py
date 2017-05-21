## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 08.10.14
#
# @todo current_DWM_values exists only for photoreceptors, not for blank
# sensors.

# modified: 31.01.16

"""
@package CompoundPye.src.system
This file holds the class System, which handles the communication between
Surroundings- and Circuit-objects.

@todo Integrate a state-save system to store the last state of the whole
circuit. This state could then be used to initialize other
circuits/systems.
"""

import numpy as np
import sys

trace_length = 500


class System:
    """This class represents the whole frame that a simulation takes
    place in; i.e. everything that exits from the simulated agent's
    point of view.

    A System instance handles communication between the two different blocks
    of a simulation: the circuit (neurons inside the animal) and the
    surroundings (what the animal can see).
    """
    def __init__(self, circuit, surroundings, dt,
                 relaxation_time=1, relaxation_intensity=0.5,
                 relax_calculation='simple_photoreceptor',
                 save_path_prefix="./", save_on_del=False):
        # Ciruit object holding all sensors and components/neurons.
        self.circuit = circuit
        # If `circuit` is a string, it needs to be the path to a
        # pickled circuit.
        if type(self.circuit) == str:
            import pickle
            with open(self.circuit, 'rb') as f:
                self.circuit = pickle.load(f)
        # Surroundings object, representing the agent/animal's surroundings.
        self.surroundings = surroundings
        # Time step dt.
        self.dt = dt

        ## NOT IN USE YET
        self.sensors_to_track = []
        ## NOT IN USE YET
        self.components_to_track = []
        ## NOT IN USE YET
        self.track_data = {'components': {}, 'sensors': {}}

        for s in self.circuit.sensors:
            s.set_dt(dt)

        # Run initial relaxation
        self.initial_relaxation(relaxation_time, relaxation_intensity, relax_calculation)

        # <boolean> If True, circuit will be pickled on destruction of
        # this system.
        self.save_on_del = save_on_del

        # Path folder in which the output will be stored.
        # Currently only used for circuit pickle in destructor.
        self.save_path_prefix = save_path_prefix
        if not self.save_path_prefix[-1] == "/":
            self.save_path_prefix += "/"

    def initial_relaxation(self, t_relax, I, mode):
        """Run relaxation in advance to the actual simulation."""
        t = 0
        if type(I) == float or type(I) == int or type(I) == np.float64:
            self.surroundings.intensities = np.ones(self.surroundings.intensities.shape) * I
        elif type(I) == np.ndarray:
            self.surroundings.intensities = I
        if mode == 'simple_photoreceptor':

            while t < t_relax:
                self.circuit.sensors[0].update(self.surroundings.intensities)
                t += self.dt
                count = 0
            sys.stdout.write('relaxation done\n')
            for i in range(1, len(self.circuit.sensors)):
                self.circuit.sensors[i].current_DWM_values = self.circuit.sensors[0].current_DWM_values
                self.circuit.sensors[i].value = self.circuit.sensors[0].value
        elif mode == 'none':
            pass
        else:
            while t < t_relax:
                self.circuit.update(self.dt, self.surroundings.intensities)
                t += self.dt
            sys.stdout.write('relaxation done\n')

    def update(self):
        """
        Update the simulation/system for one time step dt.
        The procedure is the following:
           (1) Update the surroundings of the animal,
           (2) Update the circuit of the animal, i.e.
               (2a) compute sensors response to the modified surroundings,
               (2b) every neuron/component is updated using the outputs of
                    pre-synaptic neurons of the last time step.

        @todo add tracking of components
        """
        global trace_length

        self.surroundings.update(self.dt)
        self.circuit.update(self.dt, self.surroundings.intensities)


        # @todo add tracking of components
        # The following part is unused for now.
        # But it would be nice to implement tracking and saving of data
        # centrally here, instead of doing it manually for each simulation
        # script again and again.
        for i in self.sensors_to_track:
            if list(self.track_data['sensors'].keys()).count(i):
                self.track_data['sensors'][i][:-1] = self.track_data['sensors'][i][1:]
                self.track_data['sensors'][i][-1] = self.circuit.sensors[i].get_value()
            else:
                new_array = np.zeros(trace_length)
                new_array[-1] = self.circuit.sensors[i].get_value()
                self.track_data['sensors'][i] = new_array

        for i in self.components_to_track:
            if list(self.track_data['components'].keys()).count(i):
                self.track_data['components'][i][:-1] = self.track_data['components'][i][1:]
                self.track_data['components'][i][-1] = self.circuit.components[i].get_output()
            else:
                new_array = np.zeros(trace_length)
                new_array[-1] = self.circuit.components[i].get_output()
                self.track_data['components'][i] = new_array

    def __del__(self):

        if self.save_on_del:
            import pickle
            with open(self.save_path_prefix + "circuit_on_last_time_step.pkl", 'wb') as f:
                pickle.dump(self.circuit, f, pickle.HIGHEST_PROTOCOL)

    def set_t(self, t):
        self.t = t
