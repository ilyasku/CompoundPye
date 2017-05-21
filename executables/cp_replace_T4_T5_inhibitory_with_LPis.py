#!/usr/bin/env python


import sys
print(sys.argv)

'''
@package CompoundPye.executables.cp_replace_T4_T5_inhibitory_with_LPis

Physiologically, T4 and T5 cells cannot have both excitatory and inhibitory connections, inhibitory connections to LPTCs require an inter-neuron; this script replaces negative connections from T4 and T5 cells with LPis (lobula plate intrinsic cells).
USAGE: cp_replace_T4_T5_inhibitory_with_LPis.py path/to/source/circ_file.pkl path/to/output/source_file.pkl
'''

from CompoundPye.src.Components import *
import pickle
import sys

if len(sys.argv)!=3:
    sys.stderr.write("""ERROR: wrong number of arguments.
Use it like this: 
\tcp_replace_T4_T5_inhibitory_with_LPis.py path/to/source/circ_file.pkl path/to/output/source_file.pkl""")
    sys.exit(1)
else:

    in_file=sys.argv[1]
    out_file=sys.argv[2]

    with open(in_file,'rb') as f:
        circ=pickle.load(f)

    '''
    for c in circ.components:
        print c.label
        for con in c.connections:
            print '\t'+con.target.label
    '''

    LPis=[]
    for c in circ.components:
        if c.label=="T4" or c.label=="T5":
            to_pop=[]
            for j in range(len(c.connections)):
                con=c.connections[j]
                if con.weight<0:
                    new_comp=component.Component(transfer_functions.identity,[],0.05,0.05)
                    new_comp.label="LPi_"+c.label
                    new_comp.group_label=c.group_label
                    new_comp.graph_pos=c.graph_pos
                    new_comp.attributes=c.attributes
                    new_comp.debug=c.debug
                    new_comp.add_connection(con.weight,con.target)
                    c.add_connection(1.0,new_comp)
                    LPis.append(new_comp)
                    to_pop.append(j)
            to_pop.reverse()
            for k in to_pop:
                c.connections.pop(k)


    circ.components=circ.components+LPis
    circ.create_weight_matrices()

    with open(out_file,'wb') as f:
        pickle.dump(circ,f,pickle.HIGHEST_PROTOCOL)
    



