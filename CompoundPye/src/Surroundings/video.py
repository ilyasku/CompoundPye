## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 01.12.14

"""
@package CompoundPye.src.Surroundings.video
VIDEO SUPPORT?
@todo comment file
"""

import surroundings

import numpy as np
import cv2
from gtk._gtk import Frame

class VideoSurroundings(surroundings.Surroundings):
    
    def __init__(self,video_file,intensity_dimension=1,show=False):
        

        
        self.cap=cv2.VideoCapture(str(video_file))
        
        self.ret,self.first_frame=self.cap.read()

        #w=int(self.cap.get(3))
        #h=int(self.cap.get(4))

        w=self.first_frame.shape[1]
        h=self.first_frame.shape[0]
        
        fps=self.cap.get(5)
        
        self.t=0
        
        self.ret=None
        self.show=show

        self.n_frame=0
        #self.dt=1./fps 
        ## @todo don't i need a second dt for the network/cellular calculations? this one should be too high to provide good accuracy
        
        self.intensity_dim=intensity_dimension
        
        surroundings.Surroundings.__init__(self,[w,h],intensity_dimension)
        
    def update(self,dt):
        
        self.t+=dt
        
        if self.t>(self.cap.get(0)/1000.):
            self.n_frame+=1
            #print 
            #"""
            #------------------------------------------------------------------------------------
            #------------------------------------------------------------------------------------
            #------------------------------------------------------------------------------------
            #------------------------------------------------------------------------------------
            #------------------------------------------------------------------------------------
            #------------------------------------------------------------------------------------
            #------------------------------------------------------------------------------------
            #"""
            if self.first_frame!=None:
                self.ret,frame=self.cap.read()
            else:
                frame=self.first_frame
                self.first_frame=None
            
            #print frame
            if self.intensity_dim==1:
                print frame.shape
                gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


            else:
                print 'WARNING! No color support so far (in VideoSurroundings.update)'
                gray=None
            if self.show:
                cv2.imshow('frame_input',gray)
            self.intensities[:,:,0]=gray.transpose()/255.
            if self.show:
                cv2.waitKey(1)
            del frame
            del gray
        
    def close_file(self):
        if self.show:
            self.cap.release()
        
        
