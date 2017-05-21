## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 19.01.15

"""
@package CompoundPye.src.Parser.stimuli_creator

Creates CompoundPye.src.Surroundings.Stimuli.stimulus.Stimulus objects with parameters entered in the GUI.
"""

import sys

from . import paths_to as pt

def get_two_dim_dict():
    """
    Create a dictionary containing names and paths to all valid two dimensional stimuli classes.
    @return Dictionary with name of the classes as keys and paths to their python-files as values.
    """
    d={}
    for _file in pt.paths_to_two_dim_stimuli:
        f=open(pt.here+_file,'r')
        py_lines=f.readlines()
        for row in py_lines:
            if row:
                if len(row)>5:
                    if row[:5]=='class':
                        name = row[5:].split('(')[0].split(':')[0].lstrip()
                        fpath=pt.here+_file
                        d[name]=fpath
    return d

    
two_dim_dict=get_two_dim_dict()


# -------------- import all files in two_dim_dict ---------------------
for _file in pt.paths_to_two_dim_stimuli:
    dir,slash,fname=(pt.here+_file).rpartition('/')
    dir=dir+slash
    sys.path.append(dir)
    exec('from '+fname[:-3]+' import *')

# ---------------------------------------------------------------------



def create_single_stim(obj,extend,start,velocity,args,px_x,px_y):
    """
    Create a single stimulus object with given parameters.

    All parameters need to/can be provided as strings.
    @param obj String containing the name of a Stimulus class.
    @param extend String (list/float) specifying the spatial extend of the stimulus.
    @param start String (list/float) specifying the relative position where the stimulus starts (at the beginning of the simulation).
    @param velocity String (list/float) specifying the relative speed of the stimulus moving across the surroundings.
    @param args String (list/dictionary) containing additional input parameters to the Stimulus' construnctor/__init__-function.
    @param px_x Pixel of the Surroundings on the first axis.
    @param px_y Pixel of the Surroundings on the second axis.
    @return Stimulus object.
    """
    #print 'args'
    #print args
    exec('stim='+str(obj)+'('+str(px_x)+','+str(px_y)+','+str(extend)+','+str(start)+','+str(velocity)+','+str(args)+')')
    print(stim.intensities)
    return stim

def create_stim(px_x,px_y,stim):
    """
    Create a MotionDetectorModel.Surroundings.Stimuli.stimulus.Stimulus object with parameters as provided in the set of parameters.
    @param px_x Pixel of the Surroundings on the first axis.
    @param px_y Pixel of the Surroundings on the second axis.
    @param stim Dictionary containing the stimulus' parameters.
    @return Stimulus object.
    """
    if stim['mode']=='select':
        exec('extend=['+str(stim['extend'])+']')
        exec('start=['+str(stim['starting_point'])+']')
        exec('velocity=['+str(stim['velocity'])+']')
        return create_single_stim(stim['selected_obj'],extend,start,velocity,stim['obj_args'],px_x,px_y)

