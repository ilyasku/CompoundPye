## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 31.01.16
#
# @todo At least one detailed description missing (function compute_direction_array_mean).

"""
@package CompoundPye.src.Analyzer.analyzer
Beginnings of a general data analyzer for data generated with CompoundPye.
Reads the generated .npy files from a specified folder, gives the user some options to
process and/or plot it.
"""



import matplotlib.pyplot as plt
import numpy as np
import pickle

class Analyzer:
    """
    Class to analyze data created with MotionDetectorModel. 
    Needs to be initiated with a pass to the output folder.
    """

    def __init__(self,folder):
        """
        Creates an Analyzer object.
        @param folder Path to output folder.
        """
        self.folder=folder
        self.t=np.load(folder+'/time.npy')
        self.neurons=np.load(folder+'/neurons.npy')
        self.sensors=np.load(folder+'/sensors.npy')

        self.folder=folder


    def read_directions(self,folder=''):
        """
        Neurons like T4 and T5 have an alignment or direction, depending on the position
        of those two columns from which they receive input. These directions are stored
        in directions.pkl, and read by this function.
        """
        if folder:
            pass
        else:
            folder=self.folder

        with open(folder+'/directions.pkl','rb') as f:
            self.directions=pickle.load(f)

    def read_coords(self,folder=''):
        """
        Each neuron is either in a column or a tangential cell. If it is a columnar neuron,
        it is assigned the coordinate of the photoreceptor. Coordinates of all stored
        neurons get read via this function.
        """
        if folder:
            pass
        else:
            folder=self.folder
        with open(folder+'/coords.pkl','rb') as f:
            self.coords=pickle.load(f)

    def compute_direction_arrays_mean(self,t_start,t_end):
        """
        Takes the response of each direction selective cell, and computes the total direction of motion perceived by each column.
        DETAILED DESCRIPTION MISSING!
        @param t_start Starting point of the time interval.
        @param t_end
        """
        #Implemented in v0.93 (13.02.2016)

        import sys

        unique_coords=[]
        for c in self.coords:
            if not unique_coords.count(c) and type(c)!=str:
                unique_coords.append(c)

        horizontal=np.zeros(len(unique_coords))
        vertical=np.zeros(len(unique_coords))
        
        names=self.get_neuron_names()

        for i in range(0,len(self.directions)):
            if ['HP','HN','VP','VN'].count(self.directions[i]):
                value=self.neurons[names[i]][np.where((self.t>t_start) & (self.t<t_end))].mean()

                if self.directions[i]=='HP':
                    horizontal[unique_coords.index(self.coords[i])]+=value
                elif self.directions[i]=='HN':
                    horizontal[unique_coords.index(self.coords[i])]-=value

                elif self.directions[i]=='VP':
                    vertical[unique_coords.index(self.coords[i])]+=value
                elif self.directions[i]=='VN':
                    vertical[unique_coords.index(self.coords[i])]-=value
            else:
                pass
                #sys.stderr.write("CANT UNDERSTAND DIRECTION: "+self.directions[i])

        return horizontal,vertical,unique_coords

    def convert_direction_arrays_to_arrows(self,horizontal,vertical):
        angle=np.arctan2(vertical,horizontal)
        r=np.sqrt(horizontal**2+vertical**2)
        return r,angle

    def plot_direction_arrays_as_arrows(self,ax,horizontal,vertical,coords,stretch_factor=1):
        r,angle=self.convert_direction_arrays_to_arrows(horizontal,vertical)
        
        


    def compute_direction_arrays_max(self,t_start_to_look=4):

        import sys

        unique_coords=[]
        for c in self.coords:
            if not unique_coords.count(c) and type(c)!=str:
                unique_coords.append(c)

        horizontal=np.zeros(len(unique_coords))
        vertical=np.zeros(len(unique_coords))
        
        names=self.get_neuron_names()

        for i in range(0,len(self.directions)):
            if ['HP','HN','VP','VN'].count(self.directions[i]):
                _max=self.neurons[names[i]][np.where(self.t>t_start_to_look)[0][0]:self.neurons[names[i]].shape[0]].max()
                _min=self.neurons[names[i]][np.where(self.t>t_start_to_look)[0][0]:self.neurons[names[i]].shape[0]].min()
                value=max(abs(_max),abs(_min))

                if self.directions[i]=='HP':
                    horizontal[unique_coords.index(self.coords[i])]+=value
                elif self.directions[i]=='HN':
                    horizontal[unique_coords.index(self.coords[i])]-=value

                elif self.directions[i]=='VP':
                    vertical[unique_coords.index(self.coords[i])]+=value
                elif self.directions[i]=='VN':
                    vertical[unique_coords.index(self.coords[i])]-=value
            else:
                pass
                #sys.stderr.write("CANT UNDERSTAND DIRECTION: "+self.directions[i])

        return horizontal,vertical,unique_coords
            

    def plot_directional_response(self):
        pass

    def get_neuron_names(self):
        """
        Returns the labels of all neurons (you need them to access the neuron's data).
        """
        return self.neurons.dtype.names


    def get_neuron_statistics(self,name,boundaries=[0.0,1.0]):
        """
        NOT USED SO FAR!
        Returns some statistical values (mean, std, ...) of one neuron.
        @param name Label of the neuron.
        """
        data=np.sort(self.neurons[name])[boundaries[0]*self.neurons[name].shape[0]:boundaries[1]*self.neurons[name].shape[0]]
        median=data[data.shape[0]/2]
        mean=data.mean()
        std=data.std()
        q1=data[data.shape[0]/4]
        q3=data[data.shape[0]/4*3]

    def boxplot_neuron(self,ax,pos,name,cut_off=0.15,plot_args=[],plot_kwargs={}):
        """
        Create a boxplot of a neuron's statistical values.
        @param ax axis object to plot into.
        @param pos x-coordinate at which to plot the boxplot.
        @param name Label of the neuron.
        @param cut_off Tells the function to use only the upper (1-cut_off) part of the neuron's data.
        @param plot_args List of arguments to pass on to the plot function.
        @param plot_kwargs Dictionary of keyword arguments to be passed on to the plot function.
        """
        plot_kwargs['positions']=[pos]
        lines_dict=ax.boxplot(np.sort(self.neurons[name])[int(cut_off*self.neurons[name].shape[0]):],*plot_args,**plot_kwargs)
        return lines_dict

    def plot_neuron(self,ax,name,plot_args=[],plot_kwargs={},norm_factor=1.0):
        """
        Plot a neuron's response (against time).
        @param ax Axis object to plot into.
        @param name Label of the neuron.
        @param plot_args List of arguments to pass on to the plot function.
        @param plot_kwargs Dictionary of keyword arguments to be passed on to the plot function.
        @param norm_factor Divide data by this factor.
        """

        min_shape=min(self.t.shape[0],self.neurons[name].shape[0])
        line=ax.plot(self.t[:min_shape],self.neurons[name][:min_shape]/norm_factor,*plot_args,**plot_kwargs)
        return line

    def get_sensor_names(self):
        """
        Returns the labels of all sensors (you need them to access a sensor's data).
        """
        return self.sensors.dtype.names

    def plot_sensor(self,ax,name,plot_args=[],plot_kwargs={}):
        """
        Plot a sensor's response (against time).
        @param ax Axis object to plot into.
        @param name Label of the sensor.
        @param plot_kwargs Dictionary of keyword arguments to be passed on to the plot function.
        @param norm_factor Divide data by this factor.
        """
        min_shape=min(self.t.shape[0],self.sensors[name].shape[0])
        line=ax.plot(self.t[:min_shape],self.sensors[name][:min_shape],*plot_args,**plot_kwargs)
        return line



    def plot_intensities(self,n_subplots=[1,1],subplots_args=[],subplots_kwargs={'sharex':True,'sharey':True},labels=True):
        """
        Plot surroundings' intensities at a few timestamps (number of timestamps depends on the number of subplots).
        @param n_subplots Number of rows and columns of subplots.
        @param subplots_args List of arguments to be passed on to the plot functions.
        @param subplots_kwargs Dictionary of keyword arguments to be passed on to the plot functions.
        @param labels NOT USED SO FAR.
        """
        intens=np.load(self.folder+'/intensities.npy')
        f,ax=plt.subplots(n_subplots[0],n_subplots[1],*subplots_args,**subplots_kwargs)
        n=n_subplots[0]*n_subplots[1]
        step=intens.shape[0]/n
        indices=np.arange(0,n*step,step)

        for i in range(0,n):
            ax.flat[i].imshow(intens[indices[i],:,:].transpose(),aspect='auto')

        for i in range(0,n_subplots[0]-1):
            for j in range(0,n_subplots[1]):
                for label in ax[i,j].get_xticklabels():
                    label.set_visible(False)
            
        for i in range(1,n_subplots[1]):
            for j in range(0,n_subplots[0]):
                for label in ax[j,i].get_yticklabels():
                    label.set_visible(False)

        f.subplots_adjust(hspace=0.05,wspace=0.05,right=0.98,left=0.05,bottom=0.06)
        f.suptitle('Intensities',fontsize=16)
        f.show()
        return f,ax

    def plot_intensities_ax(self,ax,i,imshow_kwargs={}):
        """
        Plot intensities at time-index i.
        @param ax Axis object to plot into.
        @param i Index (t=i*dt).
        @param imshow_kwargs Dictionary of keyword arguments to be passed on to the imshow function call.
        """
        intens=np.load(self.folder+'/intensities.npy')
        output=ax.imshow(intens[i,:,:].transpose(),aspect='auto',**imshow_kwargs)
        return intens,output
        
