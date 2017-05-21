#! python

## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 03.03.16

import pickle
import sys

# colors for commandline output
# start color with one of the strings, end it with ENDC
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

f_handle = sys.stdout


def evaluate_arg(arg, circ_object):

    arg_dict = {'-i': run_interactive, '--interactive': run_interactive,
                '--count': count, '--functions': get_functions,
                '--tau': get_time_consts, '--time-const': get_time_consts}
    if list(arg_dict.keys()).count(arg):
        arg_dict[arg](circ_object)
        return 1
    else:
        return 0


def evaluate_tuple(arg, arg_follow, circ_object):
    arg_dict = {'--connections': get_connections}
    if list(arg_dict.keys()).count(arg):
        arg_dict[arg](arg_follow, circ_object)
        return 2
    else:
        return evaluate_arg(arg, circ_object)


def get_time_consts(circ_object):
    comps = {}

    for c in circ_object.components:
        if list(comps.keys()).count(c.label):
            pass
        else:
            comps[c.label] = [c.activation_func, c.param, c.time_const_input, c.time_const_output]

    for label in comps:
        print(len(comps[label]))
        f_handle.write(label + ":\n\ttau_input: " + str(comps[label][2]) +
                       '\n\ttau_output: ' + str(comps[label][3]) + '\n\n')


def get_connections(component_name, circ_object):
    pass


def get_functions(circ_object):
    comps = {}
    for c in circ_object.components:
        if list(comps.keys()).count(c.label):
            pass
        else:
            comps[c.label] = [c.activation_func, c.param, c.time_const_input, c.time_const_output]

    for label in comps:
        f_handle.write(label + ":\n\tfunction: " + str(comps[label][0]).split()[1] +
                       '\n\tparameters: ' + str(comps[label][1]) + '\n\n')


def count(circ_object):
    counts = {}
    for c in circ_object.components:
        if list(counts.keys()).count(c.label):
            counts[c.label] = counts[c.label] + 1
        else:
            counts[c.label] = 1

    for label in counts:
        f_handle.write(label + ": " + str(counts[label]) + '\n')
        

def interactive_evaluate(input_str, circ_object):
    return 0


def run_interactive(circ_object):
    x = 1
    while x:
        x = interactive_evaluate('', circ_object)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        f_handle.write(FAIL + """ERROR: You need to provide at least the file name (.pkl) to the circuit object
""" + ENDC)
        sys.exit(1)
    else:
        print((WARNING + "loading file ..." + ENDC))
        circ_obj = pickle.load(open(sys.argv[1], 'rb'))
        if len(sys.argv) < 3:
            print((WARNING + "default output: displaying names of " 
                  + "components and \nnames of components they connect to with " 
                  + "some indentation" + ENDC))
            for c in circ_obj.components:
                f_handle.write(c.label + '\n')
                for conn in c.connections:
                    f_handle.write('\t' + conn.target.label + '\n')
        else:            
            i = 2
            while i < len(sys.argv):

                f_handle.write("""====================================
evaluating parameter """ + OKGREEN + sys.argv[i] + ENDC + "\n")
                if i < len(sys.argv) - 1:
                    msg = evaluate_tuple(sys.argv[i], sys.argv[i + 1], circ_obj)
                else:
                    msg = evaluate_arg(sys.argv[i], circ_obj)
                if msg == 2:
                    i += 1
                elif msg == 0:
                    f_handle.write(WARNING + """WARNING: cannot process parameter """ 
                                   + ENDC + OKGREEN + sys.argv[i] + ENDC + "\n")
                i += 1
