## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 15.01.15


import sys

def handle(level,msg):
    if level==0:
        pass
    elif level==1:
        sys.stdout.write('WARNING: '+msg+'. ')
        
    elif level==2:
        sys.stderr.write('ERROR: '+msg+'. ')
        sys.exit()
