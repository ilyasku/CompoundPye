#! python


"""
Run this to analyze a set of simulations conducted with the non_GUI_wrapper.py
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from CompoundPye.Analyzer.analyze_compare import AnalyzeCompare
from CompoundPye.Analyzer.analyzer import Analyzer

memory_friendly = False
_scale = 'normal'
neuron_indices = [-1]
skip = 0.6
if len(sys.argv) > 2:
    if sys.argv.count('-log'):
        _scale = 'log'

    if sys.argv.count('-i'):
        exec("neuron_indices=" + sys.argv[sys.argv.index('-i') + 1])

    if sys.argv.count('--memory-friendly'):
        memory_friendly = True

    if sys.argv.count('--skip'):
        skip = float(sys.argv[sys.argv.index('--skip') + 1])

analyze_compare_object = AnalyzeCompare(sys.argv[1], memory_friendly)
folders = analyze_compare_object.folders
speeds = analyze_compare_object.speeds

random_inds = np.random.randint(len(folders), size=2)

for i in neuron_indices:
    if memory_friendly:
        ana = Analyzer(folders[0])
        name = ana.get_neuron_names()[i]
    else:
        name = analyze_compare_object.ana_objects[0].get_neuron_names()[i]
    f_mean, ax_mean = plt.subplots(1, 1)
    analyze_compare_object.plot_mean_resp(ax_mean, name, scale=_scale, skip=skip)

ax_mean.set_title('mean')
ax_mean.grid()

plt.show()
