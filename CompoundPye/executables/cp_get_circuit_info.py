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

if __name__=="__main__":
    if len(sys.argv) < 2:
        sys.stderr.write(FAIL+"""ERROR: You need to provide at least the file name (.pkl) to the circuit object
"""+ENDC)
        sys.exit(1)
    else:
        circ_obj=pickle.load(open(sys.argv[1],'rb'))

        if len(sys.argv)<3:
            for c in circ_obj.components:
                sys.stdout.write(c.label+'\n')
                for conn in c.connections:
                    sys.stdout.write('\t'+conn.target.label+'\n')

        else:
            pass
    
