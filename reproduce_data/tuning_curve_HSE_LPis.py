import matplotlib.pyplot as plt
from CompoundPye.Analyzer import analyze_compare as ac

from matplotlib import gridspec
plt.rc('font', size=15)

## read data
path_prefix = "/media/windows/ilyas/data/tuning_curves/Tm1_Tm2_as_HPF_with_LPis/ommatidia_equatorial/runtime_35s/grating/"
ac_objects = [ac.AnalyzeCompare(path_prefix + 'lambda30deg/'),
              ac.AnalyzeCompare(path_prefix + 'lambda40deg/'),
              ac.AnalyzeCompare(path_prefix + 'lambda60deg/'),
              ac.AnalyzeCompare(path_prefix + 'lambda90deg/')]
ac_plots_kwargs = [{'linestyle': '-',
                    'color': 'darkred',
                    'marker': 'x',
                    'markersize': 8,
                    'mec': 'black',
                    'mfc': 'black',
                    'mew': 2.,
                    'label': '$\lambda=30^{\circ}$',
                    'lw': 3, 'alpha': 0.7},
                   {'linestyle': '-', 'color': 'green',
                    'marker': 'x', 'markersize': 8,
                    'mec': 'black', 'mfc': 'black',
                    'mew': 2, 'label': '$\lambda=40^{\circ}$',
                    'lw': 3, 'alpha': 0.7},
                   {'linestyle': '-', 'color': 'blue',
                    'marker': 'x', 'markersize': 8,
                    'mec': 'black', 'mfc': 'black',
                    'mew': 2, 'label': '$\lambda=60^{\circ}$',
                    'lw': 3, 'alpha': 0.7},
                   {'linestyle': '-', 'color': 'orange',
                    'marker': 'x', 'markersize': 8,
                    'mec': 'black', 'mfc': 'black',
                    'mew': 2, 'label': '$\lambda=90^{\circ}$',
                    'lw': 3, 'alpha': 0.7}]
name = ac_objects[0].ana_objects[0].get_neuron_names()[-1]

# create figure
grid = gridspec.GridSpec(8, 30)
f = plt.figure()


ax_grating_v1 = f.add_subplot(grid[0: 2, 1: 29])
ax_grating_tuning_L = f.add_subplot(grid[2: 5, :])
ax_grating_tuning_R = f.add_subplot(grid[5: 8, :], sharex=ax_grating_tuning_L)

axes_response = [ax_grating_v1]
axes_tuning = [ax_grating_tuning_L, ax_grating_tuning_R]

## ------- plot response ---------- 
plot_indices = [10, -11]
colors = ['green', 'lime']

for ind in plot_indices:
    ac_objects[1].ana_objects[ind].plot_neuron(ax_grating_v1, name,
                                               plot_kwargs={'lw': 2.5,
                                                            'label': "v=" + str(ac_objects[1].speeds[ind] * 360) + "$\/$deg/s",
                                                            'color': colors.pop()})
for ax in axes_tuning + axes_response:
    ax.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))
for ax in axes_response:
    ax.legend(loc='best', fontsize=17, ncol=2)
    ax.grid(True)
    ax.set_xlabel('time$\/$[s]', fontsize=17)
    for ticklbl in ax.get_yticklabels():
        ticklbl.set_fontsize(15)
    for ticklbl in ax.get_xticklabels():
        ticklbl.set_fontsize(15)

## -------- tuning plots -----------
x = 200

for i in range(len(ac_objects)):
    ac_i = ac_objects[i]
    ac_i.plot_mean_resp(ax_grating_tuning_L,
                        'left tangential HS',
                        plot_kwargs=ac_plots_kwargs[i],
                        min_max_speeds=[-360, 360])
    ac_i.plot_mean_resp(ax_grating_tuning_R,
                        'right tangential HS',
                        plot_kwargs=ac_plots_kwargs[i],
                        min_max_speeds=[-360, 360])
ax_grating_tuning_L.grid()
ax_grating_tuning_R.grid()

for ax in axes_tuning:
    ax.set_xlabel('stimulus speed$\/$[deg/s]', fontsize=17)
    for ticklbl in ax.get_xticklabels() + ax.get_yticklabels():
        ticklbl.set_fontsize(15)
for ticklbl in ax_grating_tuning_L.get_xticklabels():
    ticklbl.set_visible(False)
ax_grating_tuning_L.set_ylabel('mean response \nleft', fontsize=17)
ax_grating_tuning_R.set_ylabel('mean response \nright', fontsize=17)
ax_grating_tuning_L.set_xlabel('')

## ------ adjust subplots -------
f.subplots_adjust(left=0.1, right=0.985,
                  bottom=0.1, top=0.9,
                  hspace=0.67, wspace=0.15)

## ------- row labels ----------

label_pos = [0.9175, 0.5825, 0.2575]
letter_pos = [y + 0.05 for y in label_pos]

# a=f.text(0.02, letter_pos[0], 'a', fontsize=20, fontweight='bold')
# b=f.text(0.02, letter_pos[1], 'b', fontsize=20, fontweight='bold')
# c=f.text(0.02, letter_pos[2], 'c', fontsize=20, fontweight='bold')

ax_grating_v1.set_ylabel("HSE response", fontsize=17)
ax_grating_v1.set_title("$\lambda=40^{\circ}$", fontsize=17)
ax_grating_tuning_L.legend(loc="upper left", fontsize=17, ncol=2)

f.show()
