
import numpy as np




files=['_response_to_200ms.csv','_response_to_500ms.csv','_response_to_1s.csv','_response_to_steps.csv']


path=__file__.rpartition('/')[0]+'/'
if len(path)==1:
    path='.'+path


def read_neuron_responses(neuron):
    responses=[]

    for f in files:
        r=np.genfromtxt(path+neuron+f,delimiter=',')
        r=r[r[:,0].argsort()]
        r[:,0]=r[:,0]-r[0,0]
        responses.append(r)
        
    return responses
        
Tm1_responses=read_neuron_responses('Tm1')
Tm2_responses=read_neuron_responses('Tm2')


dt=0.001

t200ms=np.arange(0,max(Tm1_responses[0][-1,0],Tm2_responses[0][-1,0]),dt)
s200ms=np.ones_like(t200ms)*0.05
s200ms[np.where(((t200ms>=1.3175)&(t200ms<1.5175)))[0]]=1.0

t500ms=np.arange(0,max(Tm1_responses[1][-1,0],Tm2_responses[1][-1,0]),dt)
s500ms=np.ones_like(t500ms)*0.05
s500ms[np.where(((t500ms>=.95)&(t500ms<1.45))|((t500ms>=1.95)&(t500ms<2.45))|((t500ms>=2.95)&(t500ms<3.45))|((t500ms>=3.95)&(t500ms<4.45)))[0]]=1.0


t1s=np.arange(0,max(Tm1_responses[2][-1,0],Tm2_responses[2][-1,0]),dt) 
s1s=np.ones_like(t1s)*0.05
s1s[np.where((t1s>=1.968)&(t1s<2.968))[0]]=1.0

tsteps=np.arange(0,20.897,dt)
ssteps=np.ones_like(tsteps)*0.1
ssteps[np.where((tsteps>=1.)&(tsteps<6.))]=0.5
ssteps[np.where((tsteps>=6.)&(tsteps<11.))]=0.9
ssteps[np.where((tsteps>=11.)&(tsteps<16.))]=0.5

stims=[np.array((t200ms,s200ms)).transpose(),np.array((t500ms,s500ms)).transpose(),np.array((t1s,s1s)).transpose(),np.array((tsteps,ssteps)).transpose()]
