## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 09.10.14

"""
@package CompoundPye.src.Plotting.single_detector_plot
Provides functions to plot outputs of a single detector unit.
"""


import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import numpy as np



def plot(data,tlim=None,plot_args=[],plot_kw_args={}):
    """
    Plot output of a single detector unit.
    
    Creates a figure and several axis (sub plots). Designed to plot outputs of all elements of a Hassenstein-Reichardt-Detector.
    That is, 2 Sensors, 2 input filter, 2 low-pass filter, 2 high-pass filter, 2 multiplication units, 1 subtraction unit.
    @param data Array of outputs. Should have 11 elements in the first dimension (one row for each element of the detector), and an arbitrary number of elements in the second dimension (== number of time steps).
    @param tlim Specifies the index of the last time step that should be included in the plot.
    @param plot_args List of arguments that is passed on to pyplot's plot function.
    @param plot_kw_args Dictionary of keyword arguments that is passed on to pyplot's plot function.
    @return Tuple containing the figure-object and a list of axis-objects that were added to the figure.
    
    @note plot_args and plot_kw_args not used so far...  
    """
    
    dt=data[0][1]-data[0][0]
    if tlim==None:
        tlim=data.shape[1]
    
    print('shape:')
    print(data.shape)
    
    gs=gridspec.GridSpec(6,4)
    f=plt.figure()
    
    ax_detector1=f.add_subplot(gs[0,:2])
    ax_detector2=f.add_subplot(gs[0,2:],sharex=ax_detector1#,sharey=ax_detector1
                               )
    
    ax_input_filter1=f.add_subplot(gs[1,:2],sharex=ax_detector1)
    ax_input_filter2=f.add_subplot(gs[1,2:],sharex=ax_detector1#,sharey=ax_input_filter1
                                   )
    
                               
    
    ax_lowpass1=f.add_subplot(gs[3,:2],sharex=ax_detector1)
    ax_lowpass2=f.add_subplot(gs[3,2:],sharex=ax_detector1#,sharey=ax_lowpass1
                              )
    ax_highpass1=f.add_subplot(gs[2,:2],sharex=ax_detector1)
    ax_highpass2=f.add_subplot(gs[2,2:],sharex=ax_detector1#,sharey=ax_highpass1
                               )
    
    
    ax_multiplic1=f.add_subplot(gs[4,:2],sharex=ax_detector1)
    ax_multiplic2=f.add_subplot(gs[4,2:],sharex=ax_detector1#,sharey=ax_multiplic1
                                )
    
    ax_subtract=f.add_subplot(gs[5,1:3],sharex=ax_detector1)
    
    list_of_ax=[ax_detector1,ax_detector2,ax_input_filter1,ax_input_filter2,
                ax_lowpass1,ax_lowpass2,ax_highpass1,ax_highpass2,ax_multiplic1,ax_multiplic2,ax_subtract]
    
    list_of_colors=['red','red','blue','blue','green','green','orange','orange','brown','brown','black']
    list_of_ylabels=['sensor','input filter','low pass','high pass','multiplication','subtraction']
    list_of_titles=['pathway 1','pathway 2']
    
    for i in range(0,len(list_of_ax)):
        ax=list_of_ax[i]
        ax.plot(data[0][:tlim],data[i+1][:tlim],color=list_of_colors[i])
        if i<2:
            ax.set_title(list_of_titles[i])
        if not i%2:
            ax.set_ylabel(list_of_ylabels[i/2])
            
            
    f.subplots_adjust(left=0.06,right=0.99,wspace=0.15,hspace=0.15)
    
    return f,list_of_ax
