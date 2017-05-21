"""
So far, there is no tuning of T4/T5 cells. This is simply a script
to plot one important feature of T4 cells, that emerges when using
the network model without explicit arithmetic multiplication.
To generate the data shown in the plots, two neighbouring 
photoreceptors are used. They are stimulated with small 'steps',
where the step is shown first to the left photoreceptor, and 
with a delay to the right one. This is considered as a 
pseudo-motion of a small object from left to right.
The difference in response amplitude between left and right
T4 (or T5) cells shows that T4 (or T5) cells are motion
sensitive. 
Furthermore, T4 (and T5) cells' response is non-zero, even
for quite large delays between stimuli. This is not possible
with the simplified Hassenstein-Reichardt models, which rely
on arithmetic multiplication, resulting in zero response 
if one of the constituents is zero.
------------------------------------------------------------------
Usage:
  In an ipython command line type:
    %run T4_response_to_pseudo_motion.py <option>
------------------------------------------------------------------
Options:
  -c <path-to-circuit-file>
      Use given circuit file instead of the default file.
  -s <path-to-sensor-file>
      Use given sensor file instead of the default file.

"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(here + '/../Examples/scripts/')

import get_response_EMD


def create_stimulus_fischer_silies(t, step_delay_between_sensors, stimulus_duration=0.5,                                   
                                   offset=2, base_line=0.5, step_height=0.7):
    """
    Creates a stimulus as in Fischer et al.
    """
    intensities = np.ones((t.shape[0], 2)) * base_line
    intensities[np.where((t > offset) & (t <= offset + stimulus_duration)), 0] = step_height
    intensities[np.where((t > offset + step_delay_between_sensors + stimulus_duration) &
                         (t <= offset + step_delay_between_sensors +
                          stimulus_duration * 2)), :] = step_height
    return intensities


def gaussian_window(x, total_width=1000, sigma=100):
    gauss = np.exp(-(np.linspace(-int(total_width / 2.),
                                 int(total_width / 2.), total_width)) ** 2 / 2. / sigma ** 2)
    filtered = np.zeros_like(x)

    n = int(total_width)

    for i in range(0, len(x)):
        left = min(i, n / 2)
        right = min(len(x) - i, n / 2)
        filtered[i] = (gauss[n / 2 - left: n / 2 + right] *
                       x[i - left: i + right] / gauss[n / 2 - left: n / 2 + right].sum()).sum()

    return filtered


def create_stim_ilyas(t, step_delay_between_sensors, stim_duration=0.5, offset=2, base_line=0.5,
                      step_height=0.7, window=False, window_params=[]):
    """
    Creates a stimulus a bit different to that of Fischer et al. Instead of showing the 
    step to both sensors after the delay, it shows the step only to the second 
    sensor in this version.
    """
    intensities = np.ones((t.shape[0], 2)) * base_line
    intensities[np.where((t > offset) &
                         (t <= offset + stim_duration)), 0] = step_height
    intensities[np.where((t > offset + step_delay_between_sensors) &
                         (t <= offset + stim_duration
                          + step_delay_between_sensors)), 1] = step_height

    if window is not False:
        intensities[:, 0] = window(intensities[:, 0], *window_params)
        intensities[:, 1] = window(intensities[:, 1], *window_params)

    return intensities


if __name__ == "__main__":    
    print(("=" * 80))
    print("Running CompoundPye: script `T4_response_to_pseudo_motion`")
    print(("=" * 80))

    dt = 0.0005
    t = np.arange(0, 10, dt)
    
    delta = [0.008, 0.01, 0.05, 0.075, 0.1, 0.125, 0.3, 0.5, 1.0, 3.0]
    
    colors = ['r', 'g', 'blue', 'black', 'orange', 'lime']

    ## Be careful adding neuron labels here, or make sure the list `name_indices`
    # is corrected accordingly!
    neurons_to_store_output_of = ['T4', 'T5']

    print("creating figure and axes for plots ...")
    
    f = plt.figure()
    gs = gridspec.GridSpec(2, 3)

    ax_ex1 = f.add_subplot(gs[0, 0])
    ax_ex2 = f.add_subplot(gs[0, 1], sharey=ax_ex1)
    ax_ex3 = f.add_subplot(gs[0, 2], sharey=ax_ex1)
    ax_diff = f.add_subplot(gs[1, :])

    examples = [delta[0], delta[4], delta[-1]]
    ## make sure these indices point to the T4 cells!
    name_indices = [2, 4]
    differences = np.zeros(len(delta))

    sensor_file = get_response_EMD.default_sensor_file
    circuit_file = get_response_EMD.default_circuit_file
    if len(sys.argv) > 1:
        if sys.argv.count('-s'):
            sensor_file = sys.argv[sys.argv.index('-s') + 1]
        if sys.argv.count('-c'):
            circuit_file = sys.argv[sys.argv.index('-c') + 1]

    print(("will use sensor file at: " + sensor_file))
    print(("will use circuit file at: " + circuit_file))
    print(("-" * 80))
    print(("will run simulations for " + str(len(delta))
          + " deltas (delay between step appearance at the two different sensors) ..."))
    i = 0
    for delta_i in delta:
        print(("[%i/%i] ---- delta = %f" % (i + 1, len(delta), delta_i)))
        # uncomment the next line to create a stimulus that is more like that used in Fischer et al. 
        # intensities = create_stimulus_fischer_silies(t, delta_i, 0.05, up=0.7)
        # If you use the line above, comment out the following one.
        intensities = create_stim_ilyas(t, delta_i, 0.05)

        t, data_array, circuit = get_response_EMD.get_response(dt, intensities, 20,
                                                 neurons_to_store_output_of,
                                                 sensor_file, circuit_file)
        names = data_array.dtype.names

        differences[i] = data_array[names[name_indices[0]]].max() / data_array[
            names[name_indices[1]]].max()

        print(("ratio of maximum responses of cells '%s' and '%s': %f" %
              (names[name_indices[0]], names[name_indices[1]], differences[i])))

        if delta_i == examples[0]:
            ax_ex1.plot(t, data_array[names[name_indices[0]]], label='preferred', lw=2.2)
            ax_ex1.plot(t, data_array[names[name_indices[1]]], label='null', lw=2.2)
            ax_ex1.set_title(r'$\Delta$t=' + str(delta_i) + r'$\/$s', fontsize=16)
        elif delta_i == examples[1]:
            ax_ex2.plot(t, data_array[names[name_indices[0]]], lw=2.2)
            ax_ex2.plot(t, data_array[names[name_indices[1]]], lw=2.2)
            ax_ex2.set_title(r'$\Delta$t=' + str(delta_i) + r'$\/$s', fontsize=16)
        elif delta_i == examples[2]:
            ax_ex3.plot(t, data_array[names[name_indices[0]]], lw=2.2)
            ax_ex3.plot(t, data_array[names[name_indices[1]]], lw=2.2)
            ax_ex3.set_title(r'$\Delta$t=' + str(delta_i) + r'$\/$s', fontsize=16)
        i += 1
    
    print(("-" * 80))
    print("simulations done")
        
    ax_ex1.legend(fontsize=16)

    for ax in [ax_ex2, ax_ex3]:
        for ticklbl in ax.get_yticklabels():
            ticklbl.set_visible(False)

    for ax in [ax_ex1, ax_ex2, ax_ex3]:
        for ticklbl in (ax_ex1.get_xticklabels()
                        + ax_ex2.get_xticklabels()
                        + ax_ex3.get_xticklabels()):
            ticklbl.set_fontsize(16)
        ax.get_xticklabels()[-1].set_visible(False)

    for ticklbl in ax_ex1.get_yticklabels():
        ticklbl.set_fontsize(16)

    ax_ex2.set_xlabel(r't$\/$[s]', fontsize=16)
    ax_ex1.set_ylabel(r'response T4', fontsize=16)
    ax_diff.plot(delta, differences, color='red', marker='x', mec='black', mfc='black',
                 markersize=8, ls='dashed', lw=2.6, mew=3)
    ax_diff.set_xscale('log')

    ax_diff.set_ylabel(
        r'$\frac{\mathsf{maximum(preferred\/direction)}}{\mathsf{maximum(null\/direction)}}$',
        fontsize=27)
    ax_diff.set_xlabel(r'$\Delta$t$\/$[s]', fontsize=18.3)

    for ticklbl in ax_diff.get_xticklabels() + ax_diff.get_yticklabels():
        ticklbl.set_fontsize(16)

    ax_diff.axhline(1.0, ls=':', alpha=0.7, color='black', lw=1.5)
    f.subplots_adjust(wspace=0.02)
    f.show()

    print("finished with script `T4_response_to_pseudo_motion`")
    print(("=" * 80))
