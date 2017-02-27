"""
Example comparing the photoreceptor model to Mah et al.'s model.
One stimulus (NTSI = natural time series of intensities) and the response from their work has been digitized using WebPlotDigitizer. It gets filtered with a gaussian window, the response of the photoreceptor is calculated, and then shown together with their receptor's response in a plot.
"""

import sys
sys.path.append('../../')
import filtering

from CompoundPye.src import Sensors
from CompoundPye.src import Circuits
from CompoundPye.src import system
from CompoundPye.src import Surroundings

import numpy as np
import matplotlib.pyplot as plt


def standardize(data):
    return (data-data.mean())/data.std()

def normalize(data):
    """
    Function to normalize data to values between 0 and 1.
    @param data 1d-array to be normalized.
    @return Normalized 1d-array.
    """
    a=1/(data.max()-data.min())
    b=1-a*data.max()
    
    return a*data+b



dt=0.001 # time step
sigma=0.05 # defines width for gauss window

# -----  create photoreceptor -------
ph_r=Sensors.photoreceptor.Photoreceptor(3.0)#dt)
ph_r.set_receptive_field([1],[0],filter='pixel')
# +++++++++++++++++++++++++++++++++++

# -------- load  NTSI -----------
NTSI=np.genfromtxt('NTSI.csv',delimiter=',')
#NTSI[:,1]=NTSI[:,1]/NTSI[:,1].max()
#NTSI[:,1]=standardize(NTSI[:,1])
#NTSI[:,1]=NTSI[:,1]-NTSI[:,1].min()+NTSI[:,1].max()/1000.
# shift time axis to start at 0
NTSI[:,0]=NTSI[:,0]-NTSI[0,0]
# +++++++++++++++++++++++++++++++++++++

# ------ smooth input curve with gauss filter ------
new_t=np.arange(0,NTSI[-1,0],dt)
new_x=filtering.resample(NTSI[:,1],NTSI[:,0],new_t)
t,NTSI_filtered=filtering.window.gauss_filter(new_t,new_x,dt,sigma)
# ++++++++++++++++++++++++++++++++++++++++++++++++++


# --------- create system object ----------
# create Circuit containing only the photoreceptor
circ=Circuits.circuit.Circuit([],[ph_r])
# create Surroundings (one pixel)
surr=Surroundings.surroundings.Surroundings(1)
# create a System object with initial relaxation with first input of NTSI
syst=system.System(circ,surr,dt,10,NTSI_filtered[0])
# +++++++++++++++++++++++++++++++++++++++++


# --------- compute response -------------
response_values=np.zeros_like(t)
for i in range(t.shape[0]):
    ph_r.update(np.array([[NTSI_filtered[i]]]))
    response_values[i]=ph_r.get_value()
# ++++++++++++++++++++++++++++++++++++++++



# -------- read response of Mah et al.'s circuit ------------
circuit_resp=np.genfromtxt('mah_brinkworth_NTSI_circuit_response.csv',delimiter=',')
#circuit_resp[:,1]=normalize(circuit_resp[:,1])
#circuit_resp[:,1]=standardize(circuit_resp[:,1])
circuit_resp[:,0]=circuit_resp[:,0]-circuit_resp[0,0]
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# ---------- filter it -------------------------------------
new_t=np.arange(0,circuit_resp[-1,0],dt)
new_x=filtering.resample(circuit_resp[:,1],circuit_resp[:,0],new_t)
circ_t,circ_filtered=filtering.window.gauss_filter(new_t,new_x,dt,sigma)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



# ---------- create plot -------------------------
f,ax=plt.subplots(1,1)
ax.plot(t,standardize(response_values),ls='solid',marker='',color='red',lw=2.9,label="model's response",ms=2.5)
ax.plot(circ_t,standardize(circ_filtered),ls='solid',marker='',color='green',lw=2.9,label='Mah et al. response',ms=0.5)
ax.plot(t,standardize(NTSI_filtered),ls='dashed',marker='',color='black',lw=2.0,label="NTSI")

for ticklbl in ax.get_xticklabels()+ax.get_yticklabels():
    ticklbl.set_fontsize(15)

ax.set_ylabel('Standardized response/stimulus',fontsize=17)
ax.set_xlabel('time$\/$[s]',fontsize=17)

ax.legend(loc='best',fontsize=17)
f.show()
# +++++++++++++++++++++++++++++++++++++++++++++++
