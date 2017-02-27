import numpy as np

path=__file__.rpartition('/')[0]+'/'
if len(path)==1:
    path='.'+path


response_hard_edges_L1=np.genfromtxt(path+'response_to_hard_edges_L1_M1.csv',delimiter=',')
response_hard_edges_L2=np.genfromtxt(path+'response_to_hard_edges_L2.csv',delimiter=',')


dt=0.001
t_hard_edges=np.arange(0,8,dt)
stim_hard_edges=np.ones_like(t_hard_edges)*0.4
stim_hard_edges[np.where(((t_hard_edges>2) & (t_hard_edges <4)) | ((t_hard_edges>6)))]=0.6

if __name__=="__main__":
    import matplotlib.pyplot as plt

    f,ax=plt.subplots(3,1,sharex=True)

    ax[0].plot(response_hard_edges_L1[:,0],response_hard_edges_L1[:,1])
    ax[1].plot(response_hard_edges_L2[:,0],response_hard_edges_L2[:,1])
    ax[2].plot(t_hard_edges,stim_hard_edges)

    f.show()
