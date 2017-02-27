import numpy as np
import matplotlib.pyplot as plt



files=['_response_to_200ms','_response_to_500ms','_response_to_1s','_response_to_steps']

path=__file__.rpartition('/')[0]+'/'

if len(path)==1:
    path='.'+path


def read_neuron_responses(neuron):
    

    responses=[]

    for f in files:
        a=np.genfromtxt(path+neuron+f+'.csv',delimiter=',')
        #a[:,1]=a[:,1]-a[:,1].min()
        #a[:,1]=a[:,1]/a[:,1].max()
        responses.append(a)


    return responses


Mi1_responses=read_neuron_responses('Mi1')
Tm3_responses=read_neuron_responses('Tm3')


dt=0.001


t1s=np.arange(0,8.847,dt)
s1s=np.ones_like(t1s)*0.05
s1s[np.where((t1s>=1.964)&(t1s<2.964))[0]]=1.0



t500ms=np.arange(0,8.865,dt)
s500ms=np.ones_like(t500ms)*0.05
s500ms[np.where(((t500ms>=.967)&(t500ms<1.467))|((t500ms>=1.953)&(t500ms<2.453))|((t500ms>=2.958)&(t500ms<3.458))|((t500ms>=3.942)&(t500ms<4.442)))[0]]=1.0


t200ms=np.arange(0,5.883,dt)
s200ms=np.ones_like(t200ms)*0.05
s200ms[np.where(((t200ms>=1.7)&(t200ms<1.9)))[0]]=1.0


tsteps=np.arange(0,20.897,dt)
ssteps=np.ones_like(tsteps)*0.1
ssteps[np.where((tsteps>=0.973)&(tsteps<5.973))]=0.5
ssteps[np.where((tsteps>=5.973)&(tsteps<10.973))]=0.9
ssteps[np.where((tsteps>=10.973)&(tsteps<15.973))]=0.5


stims=[np.array((t200ms,s200ms)).transpose(),np.array((t500ms,s500ms)).transpose(),np.array((t1s,s1s)).transpose(),np.array((tsteps,ssteps)).transpose()]
