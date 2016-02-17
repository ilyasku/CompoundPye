#! python


"""
Run this to analyze a set of simulations conducted with the non_GUI_wrapper.py
"""

from CompoundPye.Analyzer.analyze_compare import *

memory_friendly=False
_scale='normal'
neuron_indices=[-1]
if len(sys.argv)>2:
    if sys.argv.count('-log'):
        _scale='log'

    if sys.argv.count('-i'):
        exec("neuron_indices="+sys.argv[sys.argv.index('-i')+1])

    if sys.argv.count('--memory-friendly'):
        memory_friendly=True


ac=AnalyzeCompare(sys.argv[1],memory_friendly)

folders=ac.folders

speeds=ac.speeds

#ana_objects=ac.ana_objects



random_inds=np.random.randint(len(folders),size=4)


for i in neuron_indices:

    if memory_friendly:
        ana=a.Analyzer(folders[0])
        name=ana.get_neuron_names()[i]
    else:
        name=ac.ana_objects[0].get_neuron_names()[i]

    f,ax=plt.subplots(1,1)
    count=0
    for ind in random_inds:
        #ana=ana_objects[ind]
        ana=a.Analyzer(folders[ind])
        ana.plot_neuron(ax,name,plot_kwargs={'label':str(speeds[ind]*360)})
        count+=1
    ax.legend()
    ax.set_title(name)

    f.show()


    f_max,ax_max=plt.subplots(1,1)
    f_abs_max,ax_abs_max=plt.subplots(1,1)
    f_mean,ax_mean=plt.subplots(1,1)

    ac.plot_max_resp(ax_max,name,scale=_scale)
    ac.plot_min_resp(ax_max,name,scale=_scale)
    ac.plot_abs_max_resp(ax_abs_max,name,scale=_scale)
    ac.plot_mean_resp(ax_mean,name,scale=_scale)

    ax_mean.set_title('mean')

    f_max.show()
    f_abs_max.show()
    f_mean.show()

