import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
import numpy as np


def create_animation(t_window,ana_object,grid_size,axis_assignment,t_start_in_seconds=4):
   
    # t_window as index, not as t in seconds

    global j

    j=np.where(ana_object.t>=t_start_in_seconds)[0][0]
 
    f=plt.figure()
    gs=gridspec.GridSpec(*grid_size)
    
    ax=[]
    lines=[]
    for i in range(len(axis_assignment)):
        ax.append(f.add_subplot(gs[axis_assignment[i][0][0]:axis_assignment[i][0][1],axis_assignment[i][1][0]:axis_assignment[i][1][1]]))
        ax[i].set_title(axis_assignment[i][3]['title'])
        ax[i].set_ylabel(axis_assignment[i][3]['ylabel'])

        for k in range(len(axis_assignment[i][2])):
            lines.append(ax[i].plot([],[],**axis_assignment[i][2][k][2])[0])
        
        if axis_assignment[i][2][k][0]=='s':
            data_y=ana_object.sensors[axis_assignment[i][2][k][1]][j:]
        else:
            data_y=ana_object.neurons[axis_assignment[i][2][k][1]][j:]
        ax[i].set_ylim(data_y.min()-np.abs(data_y.min())*0.1,data_y.max()+np.abs(data_y.max()*0.1))

        if axis_assignment[i][3]['legend']==True:
            ax[i].legend()

    cid=f.canvas.mpl_connect('button_press_event',onclick)





    def animate(n):
        global running
        global j

        #print "="*20
        #print n
        #print j


        if j<len(ana_object.t):
            dt=ana_object.t[1]-ana_object.t[0]
            offset=j-t_window
            if offset<0:
                offset_t=np.arange(offset,0)*dt
                offset_y=np.zeros_like(offset_t)
                min_t_index=0
            else:
                offset_t=np.array([])
                offset_y=np.array([])
                min_t_index=offset
                

            if running:
            #if True:
                count=0
                for i in range(len(axis_assignment)):
                    data_t=ana_object.t[offset:j]
                    if offset_t.shape[0]>0:
                        if data_t.shape[0]>0:
                            ax[i].set_xlim(offset_t[0],data_t[-1])
                        else:
                            ax[i].set_xlim(offset_t[0],offset_t[-1])
                    else:
                        ax[i].set_xlim(data_t[0],data_t[-1])
                    for k in range(len(axis_assignment[i][2])):
                        if axis_assignment[i][2][k][0]=='s':
                            data_y=ana_object.sensors[axis_assignment[i][2][k][1]][offset:j]
                        else:
                            data_y=ana_object.neurons[axis_assignment[i][2][k][1]][offset:j]
                        lines[count].set_data(np.concatenate([offset_t,data_t]),
                                              np.concatenate([offset_y,data_y]))

                        count+=1

                j+=1
                #print data_t.shape
                #print data_y.shape
                #print data_t.var()
                #print data_y.var()

        else:
            pass



        return lines

    ani=animation.FuncAnimation(f,animate,np.arange(t_window,ana_object.t.shape[0]/10.),interval=10,
                                blit=False)

    for ax_i in ax:
        ax_i.set_xlim(-1,10)
        #ax_i.set_ylim(-1e-3,1e-3)

    f.show()


j=0
running=True

def onclick(event):
    global running
    #print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
    #    event.button, event.x, event.y, event.xdata, event.ydata)
    if running:
        running=False
    else:
        running=True


    print(running)

    
