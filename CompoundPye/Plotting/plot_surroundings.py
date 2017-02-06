## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 14.11.14

"""
@package CompoundPye.src.Plotting.plot_surroundings

This package provides some functions to plot 1- and 2-dimensional surroundings (and its intensities).
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation


def animate_intensities(surr_object):
    pass

def plot_intensities(ax,intensities):
    """
    Plots the intensities of 1- or 2-dimensional surroundings.
    
    The function calls either plot_intensities_1_dim or plot_intensities_2_dim, depending on the dimension of the surroundings. 
    @param ax axis-object in which to plot the intensities.
    @param intensities Array containing the intensities for each pixel.
    @return matplotlib Line2D object for 1-dimensional surroundings, AxisImage object for 2-dimensional surroundings.
    """
    if intensities.ndim==2:
        return plot_intensities_1_dim(ax,intensities)
    elif intensities.ndim==3:
        return plot_intensities_2_dim(ax,intensities)
        
def plot_intensities_2_dim(ax,intensities):
    """
    Plots the intensities of 2-dimensional surroundings.
    @param ax axis-object in which to plot the intensities.
    @param intensities Array containing the intensities for each pixel.
    @return matplotlib AxisImage object.
    """
    if intensities.shape[2]==1:
        data=intensities[:,:,0]
    else:
        data=intensities
    data=data.transpose()
    img=ax.imshow(data,origin='lower')
    img.set_cmap('gray')
    
    return img


def plot_intensities_1_dim(ax,intensities):
    """
    Plots the intensities of 1-dimensional surroundings.
    @param ax axis-object in which to plot the intensities.
    @param intensities Array containing the intensities for each pixel.
    @return matplotlib Line2D object.
    """
    lines=[]
    for i in range(0,intensities.shape[1]):
        line=ax.plot(intensities[:,i],label='dim '+str(i))
        lines.append(line)
    return lines
    
    
    
