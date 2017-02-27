"""
Creates combined tuning plots for our rsif paper.
Data by Clark et al. (2011) and Behnia et al. (2014) was 'digitized' using the 
WebPlotDigitizer (http://arohatgi.info/WebPlotDigitizer/).
----------------------------------------------------------------------------------
Usage:
  In an ipython command line type:
    %run combined_example_L1_L2_Tm1_Tm2.py <options ...>
----------------------------------------------------------------------------------
Options:
  -c <path-to-circuit-file>
      Use given circuit file instead of the default file.
  -s <path-to-sensor-file>
      Use given sensor file instead of the default file.
"""
import numpy as np
import sys
import os
here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(here + '/reconstructed_data/')
sys.path.append(here + '/reconstructed_data/clark2011/data/')
sys.path.append(here + '/reconstructed_data/behnia2014/data/')
import similarity
from resample import resample
sys.path.append(here + '/../Examples/scripts/')
import get_response

import clark_reader

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

intensities = clark_reader.stim_hard_edges
pre_stimulus_t = 2.
intensities_pre_shown = np.ones(pre_stimulus_t / clark_reader.dt) * intensities.max()
intensities = np.concatenate([intensities_pre_shown, intensities])

dt = clark_reader.dt
t_relax = 10
store_output = ['L1', 'Tm3', 'Mi1', 'L2']

sensor_file = get_response.default_s_file
circuit_file = get_response.default_c_file
if len(sys.argv) > 1:
    if sys.argv.count('-s'):
        sensor_file = sys.argv[sys.argv.index('-s') + 1]
    if sys.argv.count('-c'):
        circuit_file = sys.argv[sys.argv.index('-c') + 1]

## ==========================================================================
## ========================= L1 and L2 ======================================
## ==========================================================================

## generate clark data/response
t_clark, data_array_clark, relax_array_clark = get_response.get_response(dt, intensities,
                                                                         t_relax, store_output,
                                                                         sensor_file, circuit_file)

## figure and axes

f = plt.figure()
gs = gridspec.GridSpec(7, 2)

## ==========================================================================
## Plot L1 and L2

ax_stim_clark = f.add_subplot(gs[0, 0])
ax_stim_clark.plot(clark_reader.t_hard_edges,
                   clark_reader.stim_hard_edges,
                   color='black', lw=2.4)
ax_stim_clark.patch.set_visible(False)
ax_stim_clark.set_frame_on(False)

ax_photor = f.add_subplot(gs[1: 3, 0], sharex=ax_stim_clark)
ax_photor.plot(t_clark - pre_stimulus_t, data_array_clark['s0'], lw=2.)

ax_L1_clark = f.add_subplot(gs[3: 5, 0], sharex=ax_stim_clark)
ax_L2_clark = f.add_subplot(gs[5: 7, 0], sharex=ax_stim_clark)

t_indices = np.where(t_clark > 2.0)
new_t = t_clark[t_indices] - 2.0
resampled_x_L1 = resample(clark_reader.response_hard_edges_L1[:, 1],
                          clark_reader.response_hard_edges_L1[:, 0], new_t)
resampled_x_L2 = resample(clark_reader.response_hard_edges_L2[:, 1],
                          clark_reader.response_hard_edges_L2[:, 0], new_t)

sim, model_z, clark_z = similarity.similarity_z(data_array_clark['L1'][t_indices],
                                                resampled_x_L1)

ax_L1_clark.plot(new_t, model_z, label='model', lw=2.)
ax_L1_clark.plot(new_t, clark_z, label='Clark', lw=2.)
ax_L1_clark.legend(loc=1, fontsize=17)
ax_L1_clark.legend(bbox_to_anchor=(1.05, 0.999), loc=1, fontsize=17)

sim, model_z, clark_z = similarity.similarity_z(data_array_clark['L2'][t_indices],
                                                resampled_x_L2)

ax_L2_clark.plot(new_t, model_z, label='model', lw=2.)
ax_L2_clark.plot(new_t, clark_z, label='Clark et al. 2011', lw=2.)

## ==========================================================================
## ========================= Tm1 and Tm2 ====================================
## ==========================================================================

## generate/read data

import behnia_reader_OFF
stimulus_index = 3

stim = behnia_reader_OFF.stims[stimulus_index]
response_Tm1 = behnia_reader_OFF.Tm1_responses[stimulus_index]
response_Tm2 = behnia_reader_OFF.Tm2_responses[stimulus_index]

intensities = stim[:, 1]

dt = behnia_reader_OFF.dt
t_relax = 10
store_output = ['L2', 'Tm1', 'Tm2']

t_OFF, data_array_OFF, relax_array_OFF = get_response.get_response(dt, intensities,
                                                                   t_relax, store_output,
                                                                   sensor_file, circuit_file)

## Plot stim and L2 
ax_stim_OFF = f.add_subplot(gs[0, 1])
ax_stim_OFF.plot(stim[:, 0], stim[:, 1], color='black', lw=2.4)
ax_stim_OFF.patch.set_visible(False)
ax_stim_OFF.set_frame_on(False)

ax_L2_OFF = f.add_subplot(gs[1: 3, 1], sharex=ax_stim_OFF)
ax_L2_OFF.plot(t_OFF, data_array_OFF['L2'], lw=2.2)

ax_Tm1 = f.add_subplot(gs[3: 5, 1], sharex=ax_stim_OFF)
resampled_x = resample(response_Tm1[:, 1], response_Tm1[:, 0], t_OFF)

sim, model_z, behnia_z = similarity.similarity_z(data_array_OFF['Tm1'],
                                                 resampled_x)

ax_Tm1.plot(t_OFF, model_z, label='model', lw=2.2)
ax_Tm1.plot(t_OFF, behnia_z, label='Behnia', lw=2.)
ax_Tm1.legend(loc='best', fontsize=17)

ax_Tm2 = f.add_subplot(gs[5: 7, 1], sharex=ax_stim_OFF)

resampled_x = resample(response_Tm2[:, 1], response_Tm2[:, 0], t_OFF)
sim, model_z, behnia_z = similarity.similarity_z(data_array_OFF['Tm2'], resampled_x)

ax_Tm2.plot(t_OFF, model_z, label='model', lw=2.2)
ax_Tm2.plot(t_OFF, behnia_z, label='Behnia', lw=2.2)

## ==========================================================================
## ========================= adjust plots ===================================
## ==========================================================================

# group axes
ax_stim = [ax_stim_clark, ax_stim_OFF]
ax_pre = [ax_photor, ax_L2_OFF]
ax_response_top = [ax_L1_clark, ax_Tm1]
ax_response_bot = [ax_L2_clark, ax_Tm2]
ax_response = ax_response_top + ax_response_bot

## ------------------ adjust stimulus axes -------------------------
ax_stim_clark.set_xlim(0, t_clark[-1])
ax_stim_clark.set_yticks([0.4, 0.6])

if stimulus_index < 3:
    ax_stim_OFF.set_yticks([0.05, 1.0])
else:
    ax_stim_OFF.set_yticks([0.1, 0.5, 0.9])
## ------------------------------------------------------------------

## ------------ hide xticklabels from all but bottom most axes ------
for ax in ax_stim + ax_pre + ax_response_top:
    for ticklbl in ax.get_xticklabels():
        ticklbl.set_visible(False)
## ------------------------------------------------------------------

## ------------- hide ticks, enlarge ticklabels of stim axes --------
for ax in ax_stim:
    ax.xaxis.set_tick_params(width=0)
    ax.yaxis.set_tick_params(width=0)
    for ticklbl in ax.get_yticklabels():
        ticklbl.set_fontsize(16)
## ------------------------------------------------------------------

## ------------- hide yticklabels of all but stimulus axes ----------
for ax in ax_pre + ax_response:
    for ticklbl in ax.get_yticklabels():
        ticklbl.set_visible(False)
## ------------------------------------------------------------------

## ==== xaxes of bottom most axes
for ax in ax_response_bot:
    ## ==== set labels
    ax.set_xlabel('time$\/$[s]', fontsize=17)
    ## ==== enlarge xticklabels
    for ticklbl in ax.get_xticklabels():
        ticklbl.set_fontsize(16)
## ====

## ==== ylabels
for ax in ax_stim:
    ax.set_ylabel('stimulus', fontsize=17)
ax_L1_clark.set_ylabel('L1', fontsize=17)
ax_L2_clark.set_ylabel('L2', fontsize=17)
ax_photor.set_ylabel('photoreceptor', fontsize=17)
ax_Tm2.set_ylabel('Tm2', fontsize=17)
ax_Tm1.set_ylabel('Tm1', fontsize=17)
ax_L2_OFF.set_ylabel('L2', fontsize=17)
## ====

## ==== 'shared' vlines for both columns
## ======== first, adjust for all but stimulus axes
for ax in ax_pre + ax_response:
    ax.yaxis.set_tick_params(width=0)
    for xtick in ax.get_xticks()[0:]:
        ax.axvline(xtick, color='black', ls='--', alpha=0.5)
## ======== second, adjust for stimulus axes
for ax in ax_stim:
    for xtick in ax.get_xticks()[1:]:
        ax.axvline(xtick, color='black', ls='--', alpha=0.5, ymin=0.0, ymax=1.0)
    for ytick in ax.get_yticks():
        ax.axhline(ytick, color='black', ls=':', alpha=0.3)
## ====

## ==== adjust spacing
f.subplots_adjust(bottom=0.1, top=0.93,
                  left=0.09, right=0.98,
                  hspace=0.08, wspace=0.21)

## ==== add letters to columns:
f.text(0.01, 0.95, "A", fontsize=17, weight='heavy')
f.text(0.51, 0.95, "B", fontsize=17, weight='heavy')

## show plot
f.show()
