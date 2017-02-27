import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np


f=plt.figure()
gs=gridspec.GridSpec(4,1)



neurons=['Tm1','Tm2']

files=['_response_to_200ms.csv','_response_to_500ms.csv','_response_to_1s.csv','_response_to_steps.csv']
#print __file__
#path=__file__.rpartition('/')[0]+'/'
path=''

fnames=[path+n+files[0] for n in neurons]

responses=[np.genfromtxt(fn_i,delimiter=',') for fn_i in fnames]
for i in range(len(responses)):
    r=responses[i]
    r=r[r[:,0].argsort()]
    responses[i]=r

s0=np.genfromtxt(path+'200ms_stim_OFF.csv',delimiter=',')
s1=np.genfromtxt(path+'200ms_stim_OFF.csv',delimiter=',')

s0=s0[s0[:,0].argsort()]
s1=s1[s1[:,0].argsort()]

ax_resp_Tm1=f.add_subplot(gs[0,0])
ax_resp_Tm1.plot(responses[0][:,0]-responses[0][0,0],responses[0][:,1])
ax_resp_Tm1.set_ylabel('Tm1')

ax_stim_Tm1=f.add_subplot(gs[1,0])
ax_stim_Tm1.plot(s0[:,0]-s0[0,0],s0[:,1])
ax_stim_Tm1.set_ylabel('stim')

ax_resp_Tm2=f.add_subplot(gs[2,0])
ax_resp_Tm2.plot(responses[1][:,0]-responses[1][0,0],responses[1][:,1])
ax_resp_Tm2.set_ylabel('Tm2')

ax_stim_Tm2=f.add_subplot(gs[3,0])
ax_stim_Tm2.plot(s1[:,0]-s1[0,0],s1[:,1])
ax_stim_Tm2.set_ylabel('stim')


f.show()

f_check,ax_check=plt.subplots(1,1)
ax_check.plot(np.arange(0,responses[0].shape[0]-1),responses[0][1:,0]-responses[0][:-1,0],label="Tm1")
ax_check.plot(np.arange(0,responses[1].shape[0]-1),responses[1][1:,0]-responses[1][:-1,0],label="Tm2")
ax_check.plot(np.arange(0,s0.shape[0]-1),s0[1:,0]-s0[:-1,0],label="s0")

ax_check.legend()

f_check.show()




