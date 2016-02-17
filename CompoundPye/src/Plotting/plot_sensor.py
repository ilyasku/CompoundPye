## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 21.10.14

"""
@package CompoundPye.src.Plotting.plot_sensor
Provides some functions to plot the outputs and receptive fields of sensors.
"""

def plot_receptive_field(ax,sensor,plot_kw_args={'color':'red','linewidth':2.0}):
    """
    Plots a receptive field of a sensor.
    
    Actual plotting happens in _plot_recptive_field_one_dim or _plot_recptive_field_two_dim, depending on the dimension of the Surroundings (and, thus, the dimension of the receptive field)
    @param ax Axis-object in which the receptive field is to be plotted.
    @param sensor Sensor of which the receptive field is to be plotted.
    @param plot_kw_args Dictionary of keyword-parameters to be passed on to the plot function.
    """
    if sensor.receptive_field.shape[0]==1:
        _plot_receptive_field_one_dim(ax,sensor,plot_kw_args)
    elif sensor.receptive_field.shape[0]==2:
        _plot_receptive_field_two_dim(ax,sensor,plot_kw_args)
        
def _plot_receptive_field_two_dim(ax,sensor,plot_kw_args):
    """
    Plots a receptive field of a sensor. 
    @param ax Axis-object in which the receptive field is to be plotted.
    @param sensor Sensor of which the receptive field is to be plotted.
    @param plot_kw_args Dictionary of keyword-parameters to be passed on to the plot function.
    """
    coords=[[sensor.receptive_field[0],sensor.receptive_field[0]+sensor.filter.shape[0]],[sensor.receptive_field[1],sensor.receptive_field[1]+sensor.filter.shape[1]]]
    ax.vlines(coords[0],coords[1][0],coords[1][1],**plot_kw_args)
    plot_kw_args['label']=''
    ax.hlines(coords[1],coords[0][0],coords[0][1],**plot_kw_args)
    
def _plot_receptive_field_one_dim(ax,sensor,plot_kw_args):
    """
    Plots a receptive field of a sensor. 
    @param ax Axis-object in which the receptive field is to be plotted.
    @param sensor Sensor of which the receptive field is to be plotted.
    @param plot_kw_args Dictionary of keyword-parameters to be passed on to the plot function.
    """
    coords=[sensor.receptive_field[0],sensor.receptive_field[0]+sensor.filter.shape[0]]
    ax.vlines(coords,0,2,**plot_kw_args)
    
    
