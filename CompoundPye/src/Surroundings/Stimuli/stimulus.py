## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 12.10.14

"""
@package CompoundPye.src.Surroundings.Stimuli.stimulus
Provides the basic Stimulus class, which can be used to add Stimuli to a Surrounding-object.

@todo check for case of 2 dimensional stimulus
@todo Stimulus.intensities needs to become iterable!
"""

import numpy as np
from PIL import Image

class Stimulus:
    """
    The basic Stimulus class, which can be used to add a Stimulus to a Surrounding-object.
    
    The user can specify the spatial extend or length of the Stimulus, which creates an array empty array of specified length/extend.
    This array can be filled with arbitrary values representing the visual intensities of the Stimulus. The array will be added to the intensities stored in a Surroundings-object.
    The Stimulus moves in the Surroundings according to the specified velocity.
    """
    def __init__(self,intensity_dim,spatial_extend,starting_point,velocity):
        """
        Initializes a Stimulus object.
        @param intensity_dim Dimension of the intensity, e.g. 1 for a bright-dark Stimulus or 3 for a RGB colored Stimulus.
        @param starting_point Index of the left-most pixel of the stimulus.
        @param velocity Stimulus velocity in pixel/time unit.
        """
    
        if type(starting_point)==int or type(starting_point)==float:
            self.position_in_space=np.array([starting_point])
        else:
            self.position_in_space=np.array(starting_point).astype(np.float32)

        #self.index_in_space=[]
        #for i in range(0,self.position_in_space.shape[0]):
            #self.index_in_space.append(int(self.position_in_space[i])) 
        self.index_in_space=self.position_in_space.astype(int)
        self.intensities=np.zeros(list(spatial_extend)+[intensity_dim])
        self.spatial_extend=spatial_extend
        self.velocity=np.array(velocity).astype(np.float32)

    def update(self,dt):
        """
        Updates the Stimulus, that is, the Stimulus moves according to its velocity.
        @param dt Time step for the update.
        """
        self.position_in_space+=self.velocity*dt
        #self.index_in_space=[]
        #for i in range(0,self.position_in_space.shape[0]):
            #self.index_in_space.append(int(self.position_in_space[i])) 
        

        self.index_in_space=self.position_in_space.astype(int)

        
class ImgStimulus(Stimulus):

    def __init__(self,intensity_dim,image,spatial_extend,starting_point,velocity):


        if spatial_extend[0]<image.size[0] and spatial_extend[1]<image.size[1]:
            image=image.resize(spatial_extend,Image.ANTIALIAS)
        elif spatial_extend[0]>image.size[0] and spatial_extend[1]>image.size[1]:
            image=image.resize(spatial_extend,Image.BICUBIC)
        else:
            image=image.resize(spatial_extend)

        if intensity_dim==1:
            
            a=np.zeros(spatial_extend+[1])
            a[:,:,0]=np.array(image.transpose(Image.ROTATE_90))/255.
        else:
            a=np.array(image.transpose(Image.ROTATE_90))/255.

        Stimulus.__init__(self,intensity_dim,spatial_extend,starting_point,velocity)
        self.intensities=a


class RenderStimulus(Stimulus):

    def __init__(self,intensity_dim,function,spatial_extend,starting_point,t_offset=0,function_args=[],function_kwargs={}):
        self.function=function
        self.args=function_args
        self.kwargs=function_kwargs
        self.t=t_offset
        Stimulus.__init__(self,intensity_dim,spatial_extend,starting_point,np.zeros(len(spatial_extend)))
        if len(self.spatial_extend)==1:
            self.xy_grid=np.arange(self.intensities.shape[0])
            #self.update=self.update_one
        else: #len(self.spatial_extend)==2:
            self.xy_grid=np.meshgrid(np.arange(self.intensities.shape[0]),np.arange(self.intensities.shape[1]))
            #self.update=self.update_two

    def update(self,dt):
        if len(self.spatial_extend)==1:
            self.update_one(dt)
        else:
            self.update_two(dt)
        #self.t=self.t+dt
        #self.intensities=self.function(self.t,self.xy_grid,**self.kwargs)

    def update_one(self,dt):
        self.t=self.t+dt
        self.intensities[:,0]=self.function(self.t,self.xy_grid,*self.args,**self.kwargs)

    def update_two(self,dt):
        self.t=self.t+dt
        self.intensities[:,:,0]=self.function(self.t,self.xy_grid,*self.args,**self.kwargs)
        
