## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 12.10.14

"""
@package CompoundPye.src.Surroundings.surroundings
Provides the basic Surroundings class, which handles the surroundings of the agent.

@todo update parameter description for intensity_dim
"""

'''
CHANGELOG

05.06.2015: v0.6 -> v0.7

05.06.2015: added function Surroundings.init_stim
'''



import numpy as np
from PIL import Image

from Stimuli import stimulus

class Surroundings:
    """
    The basic Surroundings-class handles the surroundings of the agent.
    
    It stores information about stimuli that the agent can see. 
    """
    def __init__(self,n_pixel,background=0.0,intensity_dim=1):
        """
        Initializes a Surroundings-object.
        @param n_pixel Integer or list of integers specifying the number of pixels of the surroundings.
        @param intensity_dim NEEDS SOME EXPLANATION THAT MAKES SENSE! Dimension of the surroundings, either one or two (the surroundings is actually thought of as a projection of the n-dim. surroundings to an (n-1)-dimensional hyper-plane, which is why the its dimension < 3.
        """
        
        if type(n_pixel)==int or type(n_pixel)==float:
            self.n_pixel=[n_pixel]
        else:
            self.n_pixel=list(n_pixel)
        self.ndim=len(self.n_pixel)
        

        self.intensity_dim=intensity_dim
        self.intensities=np.zeros(self.n_pixel+[intensity_dim])
        self.intensities_shape=self.intensities.shape
        ## conversion factor radian -> pixel
        self.conversion=np.zeros(self.ndim)
        for i in range(0,self.ndim):
            self.conversion[i]=self.n_pixel[i]/(2.0-i)/np.pi
            
        self.stimuli=[]

        self.background=background
            
    def set_sensor(self,sensor,center,filter_func,filter_params=[],filter_kw_params={}):
        """
        PROBABLY NOT NECCESSARY HERE.
        @todo check whether this function is ever used, or it MotionDetectorModel.Sensors.sensor.Sensor.set_receptive_field is always used directly.
        """
        sensor.set_receptive_field(center,filter_func,filter_params,filter_kw_params)
            
    def add_stimulus(self,stimulus_class,object_params,object_params_dict):
        """
        Adds a new Stimulus to the list of stimuli.
        @param stimulus_class A class to create the new Stimulus-object.
        @param object_params List of parameters to pass on to the constructor of the class.
        @param object_params_dict Dictionary of keyword-parameters to pass on to the constructor of the class.
        """
        new_stimulus=stimulus_class(*object_params,**object_params_dict)
        self.stimuli.append(new_stimulus)
        
    def array_to_stimulus(self,array_or_image,spatial_extend,starting_point,velocity):
        if type(array_or_image)==np.ndarray:
            if self.intensity_dim==1:
                try:
                    im=Image.fromarray(array_or_image[:,:,0]*255)
                except:
                    im=Image.fromarray(array_or_image*255)
            else:
                im=Image.fromarray(array_or_image*255,"RGB")
        else:
            im=array_or_image

        px_spatial_extend=[int(spatial_extend[0]*self.intensities.shape[0]),int(spatial_extend[1]*self.intensities.shape[1])]
        px_start=[int(starting_point[0]*self.intensities.shape[0]),int(starting_point[1]*self.intensities.shape[1])]
        px_velocity=[int(velocity[0]*self.intensities.shape[0]),int(velocity[1]*self.intensities.shape[1])]


        if px_spatial_extend[0]<im.size[0] and px_spatial_extend[1]<im.size[1]:
            im=im.resize(px_spatial_extend,Image.ANTIALIAS)
        elif spatial_extend[0]>im.size[0] and spatial_extend[1]>im.size[1]:
            im=im.resize(px_spatial_extend,Image.BICUBIC)
        else:
            im=im.resize(px_spatial_extend)

        if self.intensity_dim==1:
            #a=np.zeros(list(spatial_extend)+[1])
            a=np.zeros(px_spatial_extend+[1])
            a[:,:,0]=np.array(im.transpose(Image.ROTATE_90))/255.
        else:
            a=np.array(im.transpose(Image.ROTATE_90))/255.

        stim=stimulus.Stimulus(self.intensity_dim,px_spatial_extend,px_start,px_velocity)
        stim.intensities=a

        self.stimuli.append(stim)
            


    def init_stimuli(self):
        self.update(0)
            
    def update(self,dt):
        """
        Updates the Surroundings-object.
        
        Actual update happens in function Surroundings.update_one or Surroundings.update_two, depending on the input dimension of the Surroundings-object.
        @param dt Time-step of the update.
        """
        del self.intensities
        if self.ndim==1:
            self.update_one(dt)
        elif self.ndim==2:
            self.update_two(dt)

        self.intensities[np.where(self.intensities<0)]=0
        self.intensities[np.where(self.intensities>1)]=1
            
    def update_one(self,dt):
        """
        Updates the Surroundings-object (one-dimensional case).
        @param dt Time-step of the update.
        """
        
        self.intensities=np.zeros(self.intensities_shape)+self.background
        for stim in self.stimuli:
            stim.update(dt)
            #self.intensities[self.stimuli[i].index_in_space%self.n_pixel:(self.stimuli[i].index_in_space+self.stimuli[i].spatial_extend)%self.n_pixel]=self
            stim.index_in_space[0]=stim.index_in_space[0]%self.n_pixel[0]
            
            overshoot=stim.index_in_space[0]+stim.spatial_extend[0]-1-self.n_pixel[0]
            #print overshoot
            if overshoot<0:
                self.intensities[stim.index_in_space[0]:stim.index_in_space[0]+stim.spatial_extend[0]]+=stim.intensities
                
            else:
                self.intensities[stim.index_in_space[0]:]+=stim.intensities[:-overshoot-1]
                self.intensities[:overshoot+1]+=stim.intensities[stim.intensities.shape[0]-overshoot-1:]
            
    def update_two(self,dt):
        """
        Updates the Surroundings-object (two-dimensional case).
        @param dt Time-step of the update.
        """
        self.intensities=np.zeros(self.intensities_shape)+self.background
        for stim in self.stimuli:
            stim.update(dt)
            stim.index_in_space[0]=stim.index_in_space[0]%self.n_pixel[0]
            stim.index_in_space[1]=stim.index_in_space[1]%self.n_pixel[1]
            
            overshoot0=stim.index_in_space[0]+stim.spatial_extend[0]-1-self.n_pixel[0]
            overshoot1=stim.index_in_space[1]+stim.spatial_extend[1]-1-self.n_pixel[1]
            
            
            if overshoot0<0:
                if overshoot1<0:
                    self.intensities[stim.index_in_space[0]:stim.index_in_space[0]+stim.spatial_extend[0],
                                     stim.index_in_space[1]:stim.index_in_space[1]+stim.spatial_extend[1],:]+=stim.intensities
                else:
                    self.intensities[stim.index_in_space[0]:stim.index_in_space[0]+stim.spatial_extend[0],
                                     stim.index_in_space[1]:,:]+=stim.intensities[:,:-overshoot1-1,:]
                    self.intensities[stim.index_in_space[0]:stim.index_in_space[0]+stim.spatial_extend[0],
                                     :overshoot1+1,:]+=stim.intensities[:,stim.intensities.shape[1]-overshoot1-1:,:]
            else:
                if overshoot1<0:
                    self.intensities[stim.index_in_space[0]:,stim.index_in_space[1]:stim.index_in_space[1]+stim.spatial_extend[1],:]+=stim.intensities[:-overshoot0-1,:,:]
                    self.intensities[:overshoot0+1,stim.index_in_space[1]:stim.index_in_space[1]+stim.spatial_extend[1],:]+=stim.intensities[stim.intensities.shape[0]-overshoot0-1:,:,:]
                    
                else:
                    self.intensities[stim.index_in_space[0]:,stim.index_in_space[1]:,:]+=stim.intensities[:-overshoot0-1,:-overshoot1-1,:]
                    self.intensities[stim.index_in_space[0]:,:overshoot1+1,:]+=stim.intensities[:-overshoot0-1,stim.intensities.shape[1]-overshoot1-1:,:]
                    
                    self.intensities[:overshoot0+1,stim.index_in_space[1]:,:]+=stim.intensities[stim.intensities.shape[0]-overshoot0-1:,:-overshoot1-1,:]
                    self.intensities[:overshoot0+1,:overshoot1+1,:]+=stim.intensities[stim.intensities.shape[0]-overshoot0-1:,stim.intensities.shape[1]-overshoot1-1:,:]
                                     
                                     
                
                    
                    
                    
                    
                    
                    
                    
            
