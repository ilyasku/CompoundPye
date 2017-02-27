"""
Creates a plot summarizing lots of results created with a single EMD.
"""

import matplotlib.pyplot as plt
import numpy as np
from CompoundPye.Analyzer import analyze_compare

from matplotlib import gridspec

plt.rc('font', size=15)

## read data
path_prefix = "/media/windows/ilyas/data/tuning_curves/Tm1_Tm2_as_HPF/EMD/runtime_35s/grating/"
analyze_compare_objects = [analyze_compare.AnalyzeCompare(path_prefix + 'lambda30deg/'),
                           analyze_compare.AnalyzeCompare(path_prefix + 'lambda40deg/'),
                           analyze_compare.AnalyzeCompare(path_prefix + 'lambda60deg/'),
                           analyze_compare.AnalyzeCompare(path_prefix + 'lambda90deg/')]
analyze_compare_plots_kwargs = [
    {'linestyle': '-', 'color': 'darkred', 'marker': 'x', 'markersize': 8,
     'mec': 'black', 'mfc': 'black', 'mew': 2., 'label': '$\lambda=30^{\circ}$',
     'lw': 3, 'alpha': 0.7},
    {'linestyle': '-', 'color': 'green', 'marker': 'x', 'markersize': 8,
     'mec': 'black', 'mfc': 'black', 'mew': 2, 'label': '$\lambda=40^{\circ}$',
     'lw': 3, 'alpha': 0.7},
    {'linestyle': '-', 'color': 'blue', 'marker': 'x', 'markersize': 8,
     'mec': 'black', 'mfc': 'black', 'mew': 2, 'label': '$\lambda=60^{\circ}$',
     'lw': 3, 'alpha': 0.7},
    {'linestyle': '-', 'color': 'orange', 'marker': 'x', 'markersize': 8,
     'mec': 'black', 'mfc': 'black', 'mew': 2, 'label': '$\lambda=90^{\circ}$',
     'lw': 3, 'alpha': 0.7}]

name = analyze_compare_objects[0].ana_objects[0].get_neuron_names()[-1]

# create figure
grid = gridspec.GridSpec(5, 30)
f = plt.figure()
ax_grating_stim = f.add_subplot(grid[0: 2, 0: 11])
ax_grating_v1 = f.add_subplot(grid[0: 2, 15:])
ax_grating_tuning = f.add_subplot(grid[2:, :])

axes_stim = [ax_grating_stim]
axes_response = [ax_grating_v1]
axes_tuning = [ax_grating_tuning]


## ------- plot response ---------- 
plot_indices = [9, -9]
colors = ['green', 'lime']

for ind in plot_indices:
    analyze_compare_objects[1].ana_objects[ind].plot_neuron(ax_grating_v1,
                                                            name,
                                                            plot_kwargs={'lw': 2.5,
                                                                         'label': "v=" + str(analyze_compare_objects[1].speeds[ind] * 360) + "$\/$deg/s",
                                                                         'color': colors.pop()})

for ax in axes_response:
    ax.legend(loc='best', fontsize=17)
    ax.grid(True)
    ax.set_xlabel('time$\/$[s]', fontsize=17)

    for ticklbl in [ax.get_yticklabels()[-1]]:
        pass
        
    for ticklbl in ax.get_yticklabels():
        ticklbl.set_fontsize(15)

    for ticklbl in ax.get_xticklabels():
        ticklbl.set_fontsize(15)

##  -------- stimuli plots -----------

grating = np.ones((3000, 3000))
for i in range(3000):
    grating[i, :] = grating[i, :] * np.sin(np.arange(-1500, 1500) / 1500. * np.pi
                                           / 40. * 360.)
ax_grating_stim.imshow(grating, cmap='gray')


xticklabels = [str(tick) for tick in np.arange(0, 390, 90)]

for ax in axes_stim:
    ax.get_yaxis().set_visible(False)
    ax.get_xaxis().set_visible(False)
    ax.set_xticks(np.arange(0, 390, 90) * 200 / 36)
    ax.set_xticklabels(xticklabels)
    ax.patch.set_visible(False)
    ax.set_frame_on(False)
    ax.set_xlabel('')

ax_grating_stim.set_title('grating stimulus\nwavelength $\lambda=40^{\circ}$', fontsize=18)
x = 200

## -------- tuning plots -----------

for i in range(len(analyze_compare_objects)):
    analyze_compare_i = analyze_compare_objects[i]
    analyze_compare_i.plot_mean_resp(ax_grating_tuning,
                                     name,
                                     plot_kwargs=analyze_compare_plots_kwargs[i],
                                     min_max_speeds=[-360, 360])
ax_grating_tuning.grid()

for ax in axes_tuning + axes_response:
    ax.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))

for ax in axes_tuning:
    ax.set_xlabel('stimulus speed$\/$[deg/s]', fontsize=17)
    for ticklbl in ax.get_xticklabels() + ax.get_yticklabels():
        ticklbl.set_fontsize(15)

ax_grating_tuning.set_ylabel('mean response', fontsize=17)

## ------ adjust subplots -------

f.subplots_adjust(left=0.1, right=0.985, bottom=0.1,
                  top=0.9, hspace=1.0, wspace=0.15)

## ------- row labels ----------

label_pos = [0.9175, 0.5825, 0.2575]
letter_pos = [y + 0.05 for y in label_pos]

# a = f.text(0.02, letter_pos[0], 'a', fontsize=20, fontweight='bold')
# b = f.text(0.02, letter_pos[1], 'b', fontsize=20, fontweight='bold')
# c = f.text(0.02, letter_pos[2], 'c', fontsize=20, fontweight='bold')

ax_grating_v1.set_ylabel("EMD response", fontsize=17)
ax_grating_v1.set_title("$\lambda=40^{\circ}$", fontsize=17)
ax_grating_tuning.legend(loc="upper left", fontsize=17)

f.show()
