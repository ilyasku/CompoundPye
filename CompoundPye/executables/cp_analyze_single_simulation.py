#! python

"""
Run this file with an output folder as first argument to see
the surroundings' intensities at 6 timestamps and the output of one neuron.
"""

from CompoundPye.src.Analyzer.analyzer import *
import sys


folder=sys.argv[1]
a=Analyzer(folder)
#f,ax=a.plot_intensities([3,2])

#f.suptitle("Intensities at 6 different time steps",fontsize=17)
#f.canvas.draw()


## from here on analysis designed for an EMD 
# designed in Behnia's fashion

f_sum,ax_sum=plt.subplots(1,1)
l=a.plot_neuron(ax_sum,a.get_neuron_names()[-1])

ax_sum.set_title("Response of neuron '"+str(a.get_neuron_names()[-1])+"'",fontsize=17)
ax_sum.set_xlabel("time$\/$[s]",fontsize=16)

f_sum.show()
f_list=[f_sum]

if len(sys.argv)>2:
    if sys.argv[2:].count("-n"):
        index=sys.argv.index("-n")
        n=int(sys.argv[index+1])
        for i in range(1,n):
            f_i,ax_i=plt.subplots(1,1)
            l=a.plot_neuron(ax_i,a.get_neuron_names()[-i-1])
            ax_i.set_title("Response of neuron '"+str(a.get_neuron_names()[-i-1])+"'",fontsize=17)
            ax_i.set_xlabel("time$\/$[s]",fontsize=16)
            f_i.show()
            f_list.append(f_i)

    elif sys.argv[2:].count("-i"):
        index=sys.argv.index("-i")
        exec("plot_indices="+sys.argv[index+1])
        for i in plot_indices:
            if i!=-1:
                f_i,ax_i=plt.subplots(1,1)
                l=a.plot_neuron(ax_i,a.get_neuron_names()[i])
                ax_i.set_title("Response of neuron '"+str(a.get_neuron_names()[i])+"'",fontsize=17)
                ax_i.set_xlabel("time$\/$[s]",fontsize=16)
                f_i.show()
                f_list.append(f_i)

    if sys.argv[2:].count("-save"):
        for i in range(0,len(f_list)):
            f_list[i].savefig("response_"+a.get_neuron_names()[-i-1].replace(' ','_')+'.png')
        #f.savefig("intensities.png")

plt.show()
    
