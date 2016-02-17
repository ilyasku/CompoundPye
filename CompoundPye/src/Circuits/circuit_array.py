## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 01.12.14

"""
@package CompoundPye.src.Circuits.circuit_array

Provides the CircuitSensorArray class, which is similar to the basic Circuit class, but is designed such that it can handle an array of sensors as inputs.
Furthermore, it provides the option to save a video of the sensors' outputs afterwards. 
"""




import circuit
import numpy as np
import cv2
#import multiprocessing as mp

#import sys
#sys.path.append('/home/ikuhlemann/workspace/DetectorModel/v0.42/MotionDetectorModel/')
#sys.path.append('/home/ilyas/Projekte/DetectorModel/v0.42/MotionDetectorModel/')
from CompoundPye.settings import *


class CircuitSensorArray(circuit.Circuit):
    """
    Circuit that needs to be initialized with a list of Components (as the basic Circuit object) and an array of Sensors.
    
    It stores the sensors' outputs in an array and provides the option to save the outputs in a video.  
    """
    
    def __init__(self,list_of_components,array_of_sensors,debug=[]):
        """
        Initializes a CircuitSensorArray-object.
        @param list_of_components Requires a list of components with predefined connections.
        @param list_of_sensors Requires an array of sensors with predefined connections to one or more component.
        @param debug List that contains debugging keywords.
        """
        
        
        list_of_sensors=[]
        for i in range(0,array_of_sensors.shape[0]):
            for j in range(0,array_of_sensors.shape[1]):
                list_of_sensors.append(array_of_sensors[i,j])
                
        circuit.Circuit.__init__(self,list_of_components,list_of_sensors,debug)
        
        self.array_of_sensors=array_of_sensors
        
        
        self.color=False
        
        
        w=array_of_sensors.shape[1]
        h=array_of_sensors.shape[0]
        
        
        self.frame_buffer=np.zeros((n_frame_buffer,h,w))
        self.n_saved_buffers=0
        self.frame=0
        self.global_max=0
        
    def update(self,dt,intensities):
        """
        Updates the circuit.
        @param dt Time step of the update.
        @param intensities Array of the intensities of the surroundings, providing inputs to the Circuit's Sensors.
        """
        circuit.Circuit.update(self,dt,intensities)
        
        if self.color==False:
            sensor_value_array=np.zeros(self.array_of_sensors.shape)
        else:
            print 'ERROR: in CircuitSensorArray_Video.update: colors not implemented yet!'
        
        '''
        pool=mp.Pool(n_processes)
        rows=[pool.apply(_get_sensor_values_row,args=(self,x)) for x in range(0,self.array_of_sensors.shape[0])]
        for i in range(0,len(rows)):
            sensor_value_array[i,:]=rows[i]
        '''
       
        for i in range(0,self.array_of_sensors.shape[0]):
            for j in range(0,self.array_of_sensors.shape[1]):
                sensor_value_array[i,j]=self.array_of_sensors[i,j].get_value()
       
        #save frame to buffer, eventually save the buffer to a file
        self.frame_buffer[self.frame,:,:]=sensor_value_array
        self.frame+=1
        if self.frame==self.frame_buffer.shape[0]:
            self._save_buffer_to_file()
            
            
    

    
    def _save_buffer_to_file(self):
        """
        Handles the saving of buffers (arrays) to files.
        """
        np.save(buffer_dir+'buffer_file_'+str(self.n_saved_buffers), self.frame_buffer)
        self.n_saved_buffers+=1
        self.frame=0
        if self.frame_buffer.max()>self.global_max:
            self.global_max=self.frame_buffer.max()
        s=self.frame_buffer.shape
        del self.frame_buffer
        self.frame_buffer=np.zeros(s)
    
    def save_video(self,output_file,fps,log=False,color=False):
        """
        Allows to generate a video from the frames in the buffer and the saved buffer-files.
        @param output_file Name of the output file.
        @param fps Frame rate of the video that is to be created.
        @param log Set True if you want to use a logarithmic scale of the intensities shown in the video, set False otherwise.
        @param color Set False if you want a gray scale video output, set True if you want a colorful output; NOTE THAT COLOR OUTPUT IS NOT IMPLEMENTED YET! 
        """
        
        w=self.array_of_sensors.shape[1]
        h=self.array_of_sensors.shape[0]
        
        fourcc=cv2.VideoWriter_fourcc(*'HFYU')
        self.out=cv2.VideoWriter(output_file,fourcc,fps,(w,h),color)
        global_max=max(self.global_max,self.frame_buffer.max())
        for file in range(self.n_saved_buffers):
            partial_array=np.load(buffer_dir+'buffer_file_'+str(file)+'.npy')
            if log:
                partial_array=np.log(partial_array+1)*255/np.log(global_max+1)
            else:
                partial_array=partial_array*255/global_max
            partial_array=partial_array.astype(np.uint8)
            for i in range(partial_array.shape[0]):
                self.out.write(partial_array[i,:,:])
            del partial_array
        if log:
            self.frame_buffer=np.log(self.frame_buffer+1)*255/np.log(global_max+1)
        else:
            self.frame_buffer=self.frame_buffer*255/global_max
        self.frame_buffer=self.frame_buffer.astype(np.uint8)
        for j in range(0,self.frame):
            self.out.write(self.frame_buffer[j,:,:])
        self.close_file()
        
    def close_file(self):
        """
        Close the video output file.
        @todo clean saved buffer-files somehow?
        """
        self.out.release()
        #cv2.waitKey(1)
        
    '''
    def __del__(self):
        print 'deleting obj'
        import os
        os.system('rm '+buffer_dir+'*')
    '''

'''        
def _get_sensor_values_row(obj,i):
    sensor_value_row=np.zeros(obj.array_of_sensors.shape[1])
    for j in range(0,obj.array_of_sensors.shape[1]):
        sensor_value_row[j]=obj.array_of_sensors[i,j].get_value()
    return sensor_value_row
'''
