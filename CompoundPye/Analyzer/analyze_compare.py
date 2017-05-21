## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 31.01.16

## @todo example folder structure in AnalyzeCompare class description


"""
@package CompoundPye.src.Analyzer.analyze_compare
Holds the AnalyzeCompare class, designed to plot results of data 
created with cp_non_GUI_wrapper.py .
"""


import glob
import numpy as np

from . import analyzer as a


class AnalyzeCompare:
    """
    This class is designed to analyze several simulations, with exact 
    same parameters but stimulus speed.
    It expects data to be created with the file cp_non_GUI_wrapper.py, or to be arranged in the same
    way as the non-GUI wrapper would do. 
    """
    def __init__(self, path, memory_friendly=False):
        """
        Initializes and AnalyzeCompare object.
        @param path Path to folder, in which the output folders of the 
        different simulations belonging to the set to be analyzed lie.
        @param memory_friendly If True, Analyze objects of individual 
        simulations will be deleted after necessary values have been read.
        """
        self.folders = glob.glob(path + 'out*')
        self.folders.sort()
        self.speeds = np.array([float(fname.split('_')[-1]) for fname in self.folders])
        self.folders = [(self.speeds[i], self.folders[i]) for i in range(0, len(self.folders))]
        self.folders.sort()
        self.folders = [item[1] for item in self.folders]
        self.speeds.sort()
        
        self.memory_friendly = memory_friendly

        if not memory_friendly:
            self.ana_objects = [a.Analyzer(folder) for folder in self.folders]

        self.name_of_loaded_neuron = None

    def get_max_min_lines(self, neuron_name='tangential HS', skip=0.8):
        """
        Reads maximum, minimum, and mean response of one cell for each simulation.
        These values (usually only mean) can be used to plot tuning curves. 
        The default parameter changing among simulations is stimulus speed. 
        Thus, speed tuning curves can be generated this way.
        """
        
        if self.name_of_loaded_neuron == neuron_name:
            return 1
        
        max_lines = []
        min_lines = []
        mean_lines = []

        if self.memory_friendly:
            for folder in self.folders:
                ana = a.Analyzer(folder)
                length = ana.neurons.shape[0]
                max_lines.append(ana.neurons[neuron_name][int(skip * length):].max())
                min_lines.append(ana.neurons[neuron_name][int(skip * length):].min())
                mean_lines.append(ana.neurons[neuron_name][int(skip * length):].mean())
                del ana

        else:
            length = self.ana_objects[0].neurons.shape[0]
            for ana in self.ana_objects:
                max_lines.append(ana.neurons[neuron_name][int(skip * length):].max())
                min_lines.append(ana.neurons[neuron_name][int(skip * length):].min())
                mean_lines.append(ana.neurons[neuron_name][int(skip * length):].mean())

        max_lines = np.array(max_lines)
        min_lines = np.array(min_lines)
        mean_lines = np.array(mean_lines)
        
        m = 1
        m = max(abs(max_lines.max()), abs(min_lines.min()))
        max_lines = max_lines / m
        min_lines = min_lines / m

        self.max_lines = max_lines
        self.min_lines = min_lines
        self.mean_lines = mean_lines
        return m    
    
    def plot_individuals(self, ax, plot_dict, plot_kwargs_excluding_color={}, colors={}):
        """
        NOT IMPLEMENTED YET.
        plot neurons' responses for simulations with different movement speeds
        idea: plot_dict={'one neurons name':[list,of,speed,indices],
        'another neurons name':[another,list,of,indices],...}
        """
        raise NotImplementedError

    def plot_max_resp(self, ax_max, neuron_name, scale='normal',
                      plot_kwargs={'linestyle': 'dashed', 'color': 'blue',
                                   'marker': 'x', 'markersize': 6,
                                   'mec': 'black', 'mfc': 'black', 'mew': 3},
                      normalize_0_to_1=False, min_max_speeds=[-360, 360]):
        """
        Plots a tuning curve using maximum responses (AnalyzeCompare.max_lines).
        @param ax_max Axis object in which to plot.
        @param neuron_name Name of neuron to read the response from.
        @param scale 'normal' for normal scale, 'log' for logarithmic scale.
        @param plot_kwargs Dictionary of keyword parameters to be passed on to the plot function.
        @param normalize_0_to_1 If True, data will be linearly stretched and shifted to cover 
        values between 0 and 1.
        @param min_max_speeds List of lower and upper speed boundaries, 
        if you wish to inlcude only stimuli in a certain interval.
        """
        m = self.get_max_min_lines(neuron_name)
        max_lines = self.max_lines

        if normalize_0_to_1:
            x_max = max_lines.max()
            x_min = max_lines.min()
            a = 1. / (x_max - x_min)
            b = 1 - x_max * a
            max_lines = a * max_lines + b              

        ind = np.where(((self.speeds * 360 < min_max_speeds[1]) &
                        (self.speeds * 360 >= min_max_speeds[0])))[0]

        line, = ax_max.plot(self.speeds[ind] * 360., max_lines[ind], **plot_kwargs)
        
        ax_max.set_xlabel('Velocity [deg/s]', fontsize=17)
        ax_max.set_ylabel('Normalized maximum response', fontsize=17)

        if scale == 'log':
            ax_max.set_xscale('log')

        return line, m

    def plot_min_resp(self, ax_min, neuron_name, scale='normal',
                      plot_kwargs={'linestyle': 'dashed', 'color': 'blue', 'marker': 'x',
                                   'markersize': 6, 'mec': 'black', 'mfc': 'black', 'mew': 3},
                      normalize_0_to_1=False, min_max_speeds=[-360, 360], possibly_invert=False):
        """
        Plots a tuning curve using minimum responses (AnalyzeCompare.min_lines).
        @param ax_min Axis object in which to plot.
        @param neuron_name Name of neuron to read the response from.
        @param scale 'normal' for normal scale, 'log' for logarithmic scale.
        @param plot_kwargs Dictionary of keyword parameters to be passed on to the plot function.
        @param normalize_0_to_1 If True, data will be linearly stretched and shifted 
        to cover values between 0 and 1.
        @param min_max_speeds List of lower and upper speed boundaries, 
        if you wish to inlcude only stimuli in a certain interval.
        """
        m = self.get_max_min_lines(neuron_name)

        min_lines = self.min_lines

        if normalize_0_to_1:
            x_max = min_lines.max()
            x_min = min_lines.min()
            a = 1. / (x_max - x_min)
            b = 1 - x_max * a
            min_lines = a * min_lines + b

        ind = np.where(((self.speeds * 360 < min_max_speeds[1])
                        & (self.speeds * 360 >= min_max_speeds[0])))[0]
        
        ind.sort()
        
        line, = ax_min.plot(self.speeds[ind] * 360., min_lines[ind], **plot_kwargs)
        
        ax_min.set_xlabel('Velocity [deg/s]', fontsize=17)
        ax_min.set_ylabel('Normalized response', fontsize=17)

        if scale == 'log':
            ax_min.set_xscale('log')

        if min_lines.min() < 0 and possibly_invert is True:
            ax_min.invert_yaxis()

        return line, m

    def plot_abs_max_resp(self, ax, neuron_name, scale='normal',
                          plot_kwargs={'linestyle': 'dashed', 'color': 'blue',
                                       'marker': 'x', 'markersize': 6,
                                       'mec': 'black', 'mfc': 'black', 'mew': 3},
                          min_max_speeds=[-360, 360]):
        """
        Plots a tuning curve using either minimum or maximum response, 
        depending on which is the greater absolute value.
        @param ax Axis object in which to plot.
        @param neuron_name Name of neuron to read the response from.
        @param scale 'normal' for normal scale, 'log' for logarithmic scale.
        @param plot_kwargs Dictionary of keyword parameters to be passed on to the plot function.
        @param min_max_speeds List of lower and upper speed boundaries, 
        if you wish to inlcude only stimuli in a certain interval.
        """
        m = self.get_max_min_lines(neuron_name)
        abs_max = []

        for i in range(len(self.max_lines)):
            if abs(self.max_lines[i]) > abs(self.min_lines[i]):
                abs_max.append(self.max_lines[i])
            else:
                abs_max.append(self.min_lines[i])

        abs_max = np.array(abs_max)

        ind = np.where(((self.speeds * 360 < min_max_speeds[1])
                        & (self.speeds * 360 >= min_max_speeds[0])))[0]

        line, = ax.plot(self.speeds[ind] * 360., abs_max[ind], **plot_kwargs)
        
        ax.set_xlabel('Velocity [deg/s]', fontsize=17)
        ax.set_ylabel('Normalized maximum response', fontsize=17)

        if scale == 'log':
            ax.set_xscale('log')

        return line, m

    def plot_mean_resp(self, ax, neuron_name, scale='normal',
                       plot_kwargs={'linestyle': 'dashed', 'color': 'blue', 'marker': 'x',
                                    'markersize': 6, 'mec': 'black', 'mfc': 'black', 'mew': 3},
                       min_max_speeds=[-360, 360], skip=0.8, normalize=False):
        """
        Plots a tuning curve using mean responses (AnalyzeCompare.mean_lines).
        @param ax Axis object in which to plot.
        @param neuron_name Name of neuron to read the response from.
        @param scale 'normal' for normal scale, 'log' for logarithmic scale.
        @param plot_kwargs Dictionary of keyword parameters to be passed on to the plot function.
        @param normalize_0_to_1 If True, data will be linearly stretched and shifted 
        to cover values between 0 and 1.
        @param min_max_speeds List of lower and upper speed boundaries, 
        if you wish to inlcude only stimuli in a certain interval.
        """
        m = self.get_max_min_lines(neuron_name, skip)
        means = []

        for i in range(len(self.max_lines)):
            means.append(self.mean_lines[i])

        means = np.array(means)
        if normalize:
            means = means / np.abs(means).max()

        ind = np.where(((self.speeds * 360 < min_max_speeds[1])
                        & (self.speeds * 360 >= min_max_speeds[0])))[0]

        line, = ax.plot(self.speeds[ind] * 360., means[ind], **plot_kwargs)
        
        ax.set_xlabel('Velocity [deg/s]', fontsize=17)
        ax.set_ylabel('mean response', fontsize=17)

        if scale == 'log':
            ax.set_xscale('log')

        return line, m
