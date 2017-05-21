import sys
sys.path.append('../..')

import MotionDetectorModel as MDM

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from MotionDetectorModel.Components.transfer_functions import sigmoid



def get_response(background,stim_intensity,t_stim,t_relax,dt=0.001,time_const_lp3=0.1):



    # ------------------ create sensors --------------------------

    photo0=MDM.Sensors.photoreceptor.Photoreceptor(dt,True,time_const_lp3=time_const_lp3,debug=[#'Sensor.update','Photoreceptor.update'
        ])

    photo0.set_receptive_field(0,'pixel')

    # ---------------------- calculations ----------------------

    t_end=2*t_relax+t_stim

    t=np.arange(int(t_end/dt))*dt

    stim_array=np.ones((t.shape[0],1))*background
    stim_array[t_relax/dt:t_relax/dt+t_stim/dt,0]=np.ones(t_stim/dt)*stim_intensity

    data_array=np.zeros(t.shape[0])

    for i in range(0,t.shape[0]):
        #print i
        current=stim_array[i:i+1,:]
        photo0.update(current)

        data_array[i]=photo0.get_value()

    return data_array,stim_array


def plot_responses(ax,list_of_resp_stim_pairs,t):
    l=list_of_resp_stim_pairs
    

    offset=0

    for pair in l:
        ax.plot(t,pair[0]+offset,label=str(pair[1].max()))
        #offset += pair[0].max()-pair[0].min()


if __name__=='__main__':
    
    t_relax=30.0
    t_stim=3.0

    time_const_lp3=3.0

    t_end=2*t_relax+t_stim
    
    dt=0.0001

    t=np.arange(int(t_end/dt))*dt

    background=[0.000000001,0.0001]
    intensities=[0.0001,0.0022,0.0046#,0.2,0.5
                 ,0.75,1.0]
    
    resp_stim_pairs=[]

    for bg in background:
        print(bg)
        for intens in intensities:
            print(intens)
            resp_stim_pairs.append(get_response(bg,intens,t_stim,t_relax,dt,time_const_lp3))
        
    i=0
    for bg in background:
        f,ax=plt.subplots(1,1)
        plot_responses(ax,resp_stim_pairs[i*len(intensities):(i+1)*len(intensities)],t)
        ax.set_title('background='+str(bg))
        i+=1

        ax.legend()
        f.show()



