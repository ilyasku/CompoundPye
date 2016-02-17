

def _install():
    cv=False
    try:
        import cv2
        cv=True
        print "Found OpenCV libraries!"
        print "Videos as input should now in theory be supported ... buuut I didn't try that in quite some time"
    except:
        print("No OpenCV libraries found!")
        print("""Will try to set up everything to work without OpenCV.
        This means you can't use videos as input, and can't create output videos.""")
    settings_str='''#multiprocessing
n_processes=1
# video output
n_frame_buffer=300
buffer_dir=path+'MotionDetectorModel/VideoBuffer/'
    '''
    settings_str+="\ncv="+str(cv)

    import site
    import os
    os.system('mkdir -p '+site.USER_SITE)
    here=os.path.dirname(os.path.abspath(__file__))
    #here=os.getcwd()

    settings_str='path='+"'"+here+"/'\n"+settings_str

    f=open(site.USER_SITE+'/compoundpye.pth','w')
    f.write(here+'/..')
    #f.write('\n')
    #f.write(here)
    f.close()

    f_settings=open(here+'/src/settings.py','w')
    f_settings.write(settings_str)
    f_settings.close()


    import glob
    parser_path_files=glob.glob(here+"/src/Parser/paths_to_*.txt")
    for path_file in parser_path_files:
        r=open(path_file,'r')
        lines=r.readlines()
        print "========"
        print lines
        out_str=""
        for line in lines:
            if line.isspace()==False:
                tail=line.rsplit("/CompoundPye",1)[-1]
                out_str+=here+tail
                #print "+++++++"
                #print out_str

        r.close()
        w=open(path_file,'w')
        w.write(out_str)
        w.close()


if __name__=='__main__':
    
    import sys
    
    if len(sys.argv)<2:
        sys.stderr.write('''-------------------------------------------
WARNING: wrong usage of this file!
-------------------------------------------

You need to run this file with a keyword from the command line.

Keywords:
    install -- add this folder to the user's site-packages (make the module import-able from everywhere on the system),
               and configure some basic settings
''')
        sys.exit(1)
        
    else:
        if sys.argv[1]=='install':            
            _install()

        else:
            sys.stderr.write('''wrong keyword!
            
possible keywords:
    install -- add this folder to the user's site-packages (make the module import-able from everywhere on the system),
               and configure some basic settings
''')
