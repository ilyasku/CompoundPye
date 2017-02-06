## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 12.10.14

"""
@package CompoundPye.src.Surroundings
Provides classes to handle the Surroundings of an agent, and classes to create stimuli in these Surroundings.
"""
import surroundings
import one_dim

from CompoundPye import settings as _settings
if _settings.cv==True:
    import video


import Stimuli
