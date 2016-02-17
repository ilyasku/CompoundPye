## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 09.10.14

"""
@package CompoundPye.src.Components.Connections.connection
Holds the basic connection class.
"""


class Connection:
    """
    Basic connection class, with only 2 variables, self.weight and self.target.
    A component and sensor should have a list of connections, that hold objects of this class. They specify their connections to other components.
    """
    
    
    def __init__(self,weight,target):
        """
        Initializes a Connecion-object.
        @param weight Strength of the connection.
        @param target Component-object that is to be the target of the connection.
        """
        
        self.weight=weight
        self.target=target
