#! python


## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 15.01.15

"""
@package CompoundPye.executables.GUI

This module holds the RunGUI-class, which initializes the whole graphical user interface and stores the parameters the user enters. 
When creating a RunGUI-object, the QtGui-Application (and the GUI) will be started automatically. You can execute this file with *python GUI.py* to start the GUI.
"""


import numpy as np
import sys
from PyQt4 import QtGui,QtCore
import pickle
from PIL import Image

import CompoundPye as CP



from CompoundPye.src.Parser import sc,creator

class RunGUI:
    """
    RunGUI initializes the graphical user interface, which enables the user to set all simulation parameters using this interface. The user can then run the simulation by pressing the run-button.
    """
    def __init__(self,args=[]):
        """
        Called when creating a RunGUI-object.

        Calls RunGUI.init_GUI which initializes the Qt-based GUI.
        @param args Function arguments to be passed on to QtGui.QApplication.
        """

        ## False until self.apply is called for the first time.
        self.once_applied=False

        self.init_GUI(args)

    def init_GUI(self,args):
        """
        Initializes the Qt-application; creates a MotionDetectorModel.GUI.mdm_gui.MDM_GUI object.
        @param args Parameters to be passed on to QtGui.QApplication.
        """
        app=QtGui.QApplication(args)
        self.GUI=CP.GUI.main_gui.Main_GUI(self)
        self.GUI.show()
        sys.exit(app.exec_())

    def apply(self):
        """
        Creates the Circuit (Sensors and Components) and Stimuli as specified in the respective tabs of the GUI.

        This function is executed when the user clicks the 'apply'-button of the GUI.
        """


        # read a bunch of parameters from the GUI (MDM_GUI-object).
        s_settings=self.GUI.tab_list[3].editor.editor.settings
        s_variables=self.GUI.tab_list[3].editor.editor.variables
        s_defaults=self.GUI.tab_list[3].editor.editor.defaults
        sensors=self.GUI.tab_list[3].editor.editor.sensors
        arrangement=self.GUI.tab_list[2].editor.arrangement
        variables=self.GUI.tab_list[2].editor.variables
        components=self.GUI.tab_list[2].editor.neurons
        connections=self.GUI.tab_list[2].editor.connections
        receiver=self.GUI.tab_list[2].editor.receiver

        neighbour_kw_params={'manually':self.GUI.values['sensor_values']['neighbourhood_manually'],
                             'range':self.GUI.values['sensor_values']['neighbourhood_range'],
                             'max_n':self.GUI.values['sensor_values']['max_neighbours']}


        if self.GUI.tab_list[1].current_combo_str=='one dimensional array':
            px=[int(self.GUI.values['surroundings_values']['px_x'])]
        elif self.GUI.tab_list[1].current_combo_str=='two dimensional array':
            px=[int(self.GUI.values['surroundings_values']['px_x']),int(self.GUI.values['surroundings_values']['px_y'])]
        else:
            self.surroundings=CP.Surroundings.video.VideoSurroundings(self.GUI.values['surroundings_values']['input_video'],1,False)
            px=self.surroundings.n_pixel
            self.px_x,self.px_y=tuple(px)
        

        ## @var self.component_list
        # list of component-objects as created with MotionDetectorModel.Parser.creator.create_circ_lists_GUI_interface
        ## @var self.sensor_list
        # list of sensor-objects as created with MotionDetectorModel.Parser.creator.create_circ_lists_GUI_interface
        

        self.component_list,self.sensor_list,self.coords,self.angles=creator.create_circ_lists_GUI_interface(px,s_settings,s_variables,s_defaults,sensors,arrangement,variables,components,connections,receiver,neighbour_kw_params,self.GUI.values['output']['show_neighbourhood_plot'])


        """
        ## @todo implement discrimination between one- and two-dimensional surroundings/stimuli
        if '...two dim ...':
            stim_list=self.GUI.values['surroundings_values']['stimuli']['two_dim']
        

        self.stimuli=[]
        self.px_x=self.GUI.values['surroundings_values']['px_x']
        self.px_y=self.GUI.values['surroundings_values']['px_y']

        for stim in stim_list:
            if stim['show']:
                self.stimuli.append(sc.create_stim(self.px_x,self.px_y,stim))


        print '++++++ velocities ++++++'
        for stim in self.stimuli:
            
            print stim.velocity
        print '++++++++++++++++++++++++'
        """
        self.once_applied=True

    
    def run(self):
        """
        Runs the simulation with Components,Sensors and Stimuli as created in RunGUI.apply and parameters as specified in the GUI.

        This function is executed when the user hits the 'run'-button in the GUI. Note that you should hit 'apply' first after each change you do in the GUI.
        This function calls apply only if you never hit the 'apply'-button before in the current session.
        """
        
        if not self.once_applied:
            self.apply()




        self.circuit=CP.Circuits.circuit.Circuit(self.component_list,self.sensor_list)


        #self.px_x=self.GUI.values['surroundings_values']['px_x']
        #self.px_y=self.GUI.values['surroundings_values']['px_y']

        if self.GUI.tab_list[1].current_combo_str=='one dimensional array':
            self.px_x=int(self.GUI.values['surroundings_values']['px_x'])
            self.surroundings=CP.Surroundings.surroundings.Surroundings((int(self.px_x)))
        elif self.GUI.tab_list[1].current_combo_str=='two dimensional array':
            self.px_x,self.px_y=(int(self.GUI.values['surroundings_values']['px_x']),int(self.GUI.values['surroundings_values']['px_y']))
            self.surroundings=CP.Surroundings.surroundings.Surroundings((int(self.px_x),int(self.px_y)))
        else:
            pass
        
        #self.surroundings=CP.Surroundings.surroundings.Surroundings((int(self.px_x),int(self.px_y)))

        ## @todo implement discrimination between one- and two-dimensional surroundings/stimuli
        if '...two dim ...':
            stim_list=self.GUI.values['surroundings_values']['stimuli']['two_dim']
        

        self.stimuli=[]

        for stim in stim_list:
            if stim['show']:
                if stim['mode']=='select':
                    self.surroundings.stimuli.append(sc.create_stim(self.px_x,self.px_y,stim))
                elif stim['mode']=='def':
                    if str(stim['def'])[:15]=="define an array":
                        pass
                    else:
                        exec(str(stim['def']))
                        exec('extend=['+str(stim['extend'])+']')
                        exec('start=['+str(stim['starting_point'])+']')
                        exec('velocity=['+str(stim['velocity'])+']')
                        self.surroundings.array_to_stimulus(a,extend,start,velocity)
                elif stim['mode']=='load':
                    if stim['load'][1]=='array':
                        a=np.load(stim['path_to_file'])
                    else:
                        a=Image.open(str(stim["path_to_file"]))
                    exec('extend=['+str(stim['extend'])+']')
                    exec('start=['+str(stim['starting_point'])+']')
                    exec('velocity=['+str(stim['velocity'])+']')
                    self.surroundings.array_to_stimulus(a,extend,start,velocity)
                    
                        
        
                else:
                    EH.handle(1,'in Parser.stimuli_creator.create_stim: not implemented yet!\n')




        
        #self.surroundings.stimuli=self.stimuli

        self.surroundings.init_stimuli()
        
        if True:

            import matplotlib.pyplot as plt
            f_check_init_stim,ax_check_init_stim=plt.subplots(1,1)
            ax_check_init_stim.imshow(self.surroundings.intensities[:,:,0].transpose())
            f_check_init_stim.show()


        with open(str(self.GUI.values['output']['dir'])+'/circuit_object.pkl','wb') as f:
            pickle.dump(self.circuit,f,pickle.HIGHEST_PROTOCOL)
        if self.GUI.tab_list[1].current_combo_str!='video input':
            with open(str(self.GUI.values['output']['dir'])+'/surroundings_object.pkl','wb') as f:
                pickle.dump(self.surroundings,f,pickle.HIGHEST_PROTOCOL)
        else:
            sys.stdout.write("""

NO WAY TO SAVE VIDEOSURROUNDINGS IMPLEMENTED SO FAR!!!!

""")


        values_text=open(str(self.GUI.values['output']['dir'])+'/values.txt','w')
        values_text.write(str(self.GUI.values))
        values_text.close()

        with open(str(self.GUI.values['output']['dir'])+'/values.pkl','wb') as f:
            pickle.dump(self.GUI.values,f,pickle.HIGHEST_PROTOCOL)


        #for stim in self.surroundings.stimuli:
            #print stim.intensities
        

        dt=self.GUI.values['system_values']['dt']
        relax_time=self.GUI.values['system_values']['relaxation_time']
        relax_intensity=self.GUI.values['system_values']['relaxation_intensity']
        relax_calculation=self.GUI.values['system_values']['relax_calculation']


        self.system=CP.system.System(self.circuit,self.surroundings,dt,relax_time,relax_intensity,relax_calculation)
    

        with open(str(self.GUI.values['output']['dir'])+'/circuit_object_relaxed.pkl','wb') as f:
            pickle.dump(self.circuit,f,pickle.HIGHEST_PROTOCOL)

        


        t=0
        t_end=float(self.GUI.values['system_values']['sim_time'])
        dt=float(self.GUI.values['system_values']['dt'])


        comps=[]

        if str(self.GUI.values['output']['n_by_index'])=='':
            comps=self.circuit.components[:]
        else:
            exec('comp_index_list='+str(self.GUI.values['output']['n_by_index']))
            comps=comps+[self.circuit.components[i] for i in comp_index_list]

        if str(self.GUI.values['output']['n_by_label'])=='':
            comps=self.circuit.components[:]
        else:
            exec('label_list='+str(self.GUI.values['output']['n_by_label']))
            for c in self.circuit.components:
                if label_list.count(c.label):
                    comps.append(c)
            
        directions=[c.direction for c in comps]

        with open(str(self.GUI.values['output']['dir'])+'/directions.pkl','wb') as f:
            pickle.dump(directions,f,pickle.HIGHEST_PROTOCOL)

        coords=[]
        for k in range(len(comps)):
            if type(comps[k].graph_pos)!=str:
                coords.append(tuple(comps[k].graph_pos))
            else:
                coords.append(comps[k].graph_pos)

        #np.save(str(self.GUI.values['output']['dir'])+'/coords.npy',coords)
        with open(str(self.GUI.values['output']['dir'])+'/coords.pkl','wb') as f:
            pickle.dump(coords,f,pickle.HIGHEST_PROTOCOL)

        labels=[(str(c.group_label),str(c.label),str(c.graph_pos)) for c in comps]
        dtypes=[(lbl[0]+' '+lbl[1],'float') for lbl in labels]

        sensors=[]
        if str(self.GUI.values['output']['s_by_index'])=='':
            sensors=self.circuit.sensors
        else:
            exec('sensors_index_list='+str(self.GUI.values['output']['s_by_index']))
            sensors=sensors+[self.circuit.sensors[i] for i in sensors_index_list]

        dtype_sensors=[(str(s.label),'float') for s in sensors]


        if str(self.GUI.values['output']['intensities_interval'])=='':
            record_interval=3000
        else:
            record_interval=int(self.GUI.values['output']['intensities_interval'])
        
        

        # creates the arrays to store the Circuit's output
        output_comp=np.zeros((int(t_end/dt)+1,),dtype=dtypes)
        output_sens=np.zeros((int(t_end/dt)+1,),dtype=dtype_sensors)
        output_surround=np.zeros((int((int(t_end/dt))/record_interval)+1,self.system.surroundings.intensities.shape[0],self.system.surroundings.intensities.shape[1]))
        i=0
    

        sys.stdout.write('\n\n\n')
        # the actual update-steps of the simulation are conducted in the following loop
        while t<t_end:
            #print '------ '+str(i)
            if i%200==0:
                sys.stdout.write('\r')
                sys.stdout.flush()
                sys.stdout.write('------ t='+str(t))
                #sys.stdout.write(str(self.system.circuit.sensors[0].get_value())+'\n')
                #sys.stdout.write(str(self.system.circuit.sensors[1].get_value())+'\n')
                #sys.stdout.write(str(self.surroundings.intensities.max())+" , "+str(self.surroundings.intensities.min())+"\n")
                #sys.stdout.write('='*30+'\n')
                #sys.stdout.write(str(self.surroundings.stimuli[1].position_in_space)+"\n")
                #sys.stdout.write(str(self.surroundings.stimuli[1].velocity)+"\n")
                #sys.stdout.write(str(self.system.surroundings.stimuli[0].position_in_space)+'\n')
            #self.system.update()
            new_comp_values=np.zeros(len(comps))
            for j in range(0,new_comp_values.shape[0]):
                new_comp_values[j]=comps[j].get_output()
                
            new_sens_values=np.zeros(len(sensors))
            for k in range(0,new_sens_values.shape[0]):
                new_sens_values[k]=sensors[k].get_value()
            #if i%200==0:
                #print new_sens_values
            output_comp[i]=new_comp_values
            output_sens[i]=new_sens_values

            if i%record_interval==0:
                #print '='*30
                #print self.system.surroundings.intensities.shape
                output_surround[i/record_interval]=self.system.surroundings.intensities[:,:,0]
            self.system.update()

            t+=dt
            i+=1
        
        # saves the output arrays in the folder you specified in the GUI's output-tab.
        np.save(str(self.GUI.values['output']['dir'])+'/neurons.npy',output_comp)
        np.save(str(self.GUI.values['output']['dir'])+'/sensors.npy',output_sens)
        np.save(str(self.GUI.values['output']['dir'])+'/intensities.npy',output_surround)
        np.save(str(self.GUI.values['output']['dir'])+'/time.npy',np.arange(0,i+1)*dt)

        self.GUI.tab_list[2].editor.save_file(str(self.GUI.values['output']['dir'])+'/circuit_file.txt')
        self.GUI.tab_list[3].editor.editor.do_save(str(self.GUI.values['output']['dir'])+'/sensor_file.txt')

        del output_surround
        del output_sens
        del output_comp

        

        

if __name__=='__main__':
    run=RunGUI(sys.argv)
