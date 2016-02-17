## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 20.01.15


"""
@package CompoundPye.src.Parser.sensor_parser

Parses sensor information from a sensor-file or save sensor information (also from the GUI) to a sensor-file.
"""


#from ..ErrorHandling import handle
#import CompoundPye.src.ErrorHandling as EH
from ...src import EH

def save_file(fname,settings,variables,defaults,sensors):
    """
    Save given sensors and their parameters to a sensor file (text file).
    @param fname Name of target file.
    @param settings Global settings to be stored in the header of the sensor file.
    @param variables Global variables to be stored in the header of the sensor file
    @param defaults Global defaults to be stored in the header of the sensor file.
    """
    f=open(fname,'w')
    

    print variables

    fstring=''
    for key in settings:
        line=key+'='+settings[key]+'\n'
        fstring=fstring+line
    for var in variables.keys():
        line='variable '+var+'='+str(variables[var])+'\n'
        fstring=fstring+line
    for d in defaults:
        line='default '+d+'='+defaults[d]+'\n'
        fstring=fstring+line

    fstring=fstring+'sensors{\n'

    for s in sensors:
        for key in s.keys():
            if s[key]=='' or str(s[key]).isspace():
                s[key]='-'
        sline=s['x']+'\t'+s['y']+'\t'+str(s['name']).replace(' ','_')+'\t'+s['sensor']+'\t'+s['obj_args']+'\t'
        sline=sline+s['filter']+'\t'+s['filter_args']+'\t'+s['neighbourhood']+'\n'
        fstring=fstring+sline
    fstring=fstring+'}'
        
    f.write(fstring)
    f.close()
    


def parse_file(fname):
    """
    Parse a sensor file to several dictionaries.
    @param fname Name of the source file.
    """
    f=open(fname,'r')
    complete_string=f.read()
    header,sections=separate_sections(complete_string)
    settings,variables,defaults=parse_header(header)
    sensors=None
    for i in range(0,len(sections)):
        if sections[i][0]=='sensors':
            sensors=parse_sensor_section(sections[i][1])
    if sensors==None:
        EH.handle(1,'Did not find the sensors-section in file '+str(fname))
        
    return settings,variables,defaults,sensors

def separate_sections(s):
    """
    Separate the complete string of a sensor file into header and different sections.
    """
    first_split=s.split('{')
    header=first_split[0].split('\n')
    first_split=first_split[1:]
    first_split.insert(0,header[-1])
    sections=[]
    section_name=first_split[0]
    for i in range(1,len(first_split)):
        split_i=first_split[i].split('}')
        sections.append([section_name,split_i[0]])
        section_name=split_i[1].lstrip()
    header=header[:-1]
    return header,sections


def parse_header(h):
    """
    Parse the settings,variables and defaults to 3 different dictionaries.
    @param h Header string.
    @return 3 separate dictionaries in the following order: settings, variables, defaults.
    """
    settings={}
    variables={}
    defaults={}
    for line in h:
        if line:
            if line.lstrip()[0]=='#':
                pass
            else:
                if line.count('='):
                    var=False
                    if len(line)>9:
                        if line[:9]=='variable ':
                            var=True
                            name,value=line[9:].split('=')
                            name=name.lstrip().rstrip()
                            variables[name]=float(value)
                    if var==False:
                        default=False
                        if len(line)>8:
                            if line[:8]=='default ':
                                default=True
                                name,value=line[8:].split('=')
                                name=name.lstrip().rstrip()
                                value=value.lstrip().rstrip()
                                defaults[name]=value
                        if default==False:
                            name,value=line.split('=')
                            name=name.lstrip().rstrip()
                            value=value.lstrip().rstrip()
                            settings[name]=value
                
    return settings,variables,defaults


def parse_sensor_section(s):
    """
    Parse a sensor section to a dictionary, in which one key represents one sensor, its value holds the sensor's parameters.
    @param s String of the sensor section.
    @return Dictionary in which keys represent sensors, their values hold the sensors' parameters.
    """
    d={}
    lines=s.split('\n')
    for line in lines:
        if line:
            if not line.lstrip()[0]=='#':
                parse_sensor_line(line,d)
    return d

def parse_sensor_line(l,d):
    """
    Parse a single line of a sensor section (= parameters for a single sensor) to a dictionary.
    @param l One line of text from a sensor section.
    @param d Pointer to the dictionary in parse_sensor_section, to which the new dicionary containing one sensor's parameters will be added.
    """
    split=l.split()
    label=split[2]
    if label=='-':
        label='('+split[0]+','+split[1]+')'
    d[label]={}
    d[label]['x']=split[0]
    d[label]['y']=split[1]
    d[label]['sensor']=split[3]
    d[label]['obj_args']=split[4]
    d[label]['filter']=split[5]
    d[label]['filter_args']=split[6]
    d[label]['neighbourhood']=split[7]
        
    
