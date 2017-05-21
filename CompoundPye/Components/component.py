## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 09.10.14

# last update 23.10.2015

"""
@package CompoundPye.src.Components.component
Holds the basic Component class.
"""


from .Connections import connection


class Component:
    """
    Basic component class.

    A Component-object is a basic building block of a circuit. It has a list of
    connections, which contains connections to other Component-objects.
    Based on the connections between components of a circuit/network, the
    Circuit-object calculates the input to each Component during one update
    step. The Component uses the input to update its internal value/membrane
    potential (self.value). It generates an output based on self.value using
    its Component.activation_func .
    """

    def __init__(self, activation_function, function_parameters=[],
                 time_const_input=0.05, time_const_output=0.05, debug=False):
        """
        Initializes a Component-object.
        @param activation_function Transfer function that is to be used to
        generate the Component's output Component.output from its internal
        value Component.value .
        @param function_parameters List of parameters for the Component's
        transfer function Component.activation_func .
        @param time_const_input Time constant for updating input.
        @param time_const_output Time constant for updating output.
        @param debug Set False, if you don't want to see debugging output,
        set True if you want to see debugging output.
        """
        # Current internal value.
        self.value = 0
        # Current output of the object, calculated using the object's transfer
        # function Component.activation_func and its internal value
        # Component.value as the function's input.
        self.output = 0

        # Transfer function of the Component-object.
        self.activation_func = activation_function
        # List of parameters for the object's transfer function
        # Component.activation_func.
        self.param = function_parameters
        # The Component's time constant, which specifies how much of its
        # previous Component.value remains after each update step.
        self.time_const_output = time_const_output
        self.time_const_input = time_const_input
        self.connections = []

        self.index_in_circuit_list = None
        # @note changed self.tag to self.label --> any errors?
        self.label = ''
        self.group_label = ''
        self.graph_pos = [0, 0]
        self.direction = ''

        # assign attributes to the neuron, e.g. axis:horizontal or axis:
        # vertical, direction:positive or direction:negative
        # (probably required for further connection)
        self.attributes = {'axis': None, 'direction': None,
                           'ipsi': None, 'contra': None}

        # create only once per pairs of neighbours, True or False
        self.next_neighbour_single_time = False

        self.debug = debug

    def update(self, input, dt):
        """
Updates the Component's internal value and output based on the provided input.
@param input Input used for update.
@param dt Time step for the update
        """

        self.value += dt / self.time_const_input * (-self.value + input)
        self.output += dt / self.time_const_output * (-self.output + self.activation_func(self.value,*self.param))

    def get_output(self):
        """
        Returns Component.output .
        """
        return self.output

    def add_connection(self, weight, target):
        """
        Adds a connections to the Component's list of connections.
        @param weight Strength of the connection.
        @param target Target of the connections (has to be a Component-object).
        """
        new_connection = connection.Connection(weight, target)
        self.connections.append(new_connection)


class Component2(Component):
    """
Very similar to the class Component, but with 2 functions in the transfer from
input to output. I'm not sure about the mathematical implications, though.
If I require 2 functions, I can as well combine them into one ...
    """
    def __init__(self, transfer_function, transfer_function_parameters,
                 activation_function, activation_function_parameters=[],
                 time_const_input=0.05, time_const_output=0.05,
                 debug=False):
        Component.__init__(self, activation_function,
                           activation_function_parameters, time_const_input,
                           time_const_output, debug)
        self.transfer_func = transfer_function
        self.trans_func_param = transfer_function_parameters
        self.act_func_param = activation_function_parameters

    def update(self, input, dt):
        self.value += dt / self.time_const_input * (-self.value + self.activation_func(input, *self.act_func_param))
        self.output +=dt / self.time_const_output * (-self.output + self.transfer_func(self.value,*self.trans_func_param))


def identity(x, gain=1.0):
    """
    Linear function that can be used as a Component's transfer function.
    @return x*gain == input times gain
    """
    return x * gain


def quadratic(x, a=1, b=0):
    """
    Quadratic function that can be used as a Component's transfer function.
    @return output of the quadratic function (a*x^2+b)
    """
    return a * x**2 + b


def power_law(x, a, b=1, c=0):
    """
    Power law that can be used as a Component's transfer function.
    @return Output produced by the power law defined through b*x^a+c.
    """
    return b * x ** a + c
