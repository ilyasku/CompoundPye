# How to reproduce the data of publication XY

## Plots in **figure 3** - T4 response to pseudo motion

Execute the script `T4_response_to_pseudo_motion.py`. This will generate the same plot as seen in the publication. Have a look into the script to see how the data is generated.

## Plots in **figure 4** - Tuning curve EMD

#### Generating the data
**BEWARE: this will roughly produce 11 GB of data.**  
  
The plot script `tuning_curve_EMD.py` requires you to have the data of the EMD simulations in a folder with several subfolders.
There needs to be one subfolder for each grating size, named `lambda<wavelength>deg` (<wavelength> should be 30, 40, 60 and 90, which are the wavelengths I used for the plots).
In each of those subfolders, there needs to be one folder for each simulation (i.e., one folder for each stimulus speed) run with a grating of that wavelength. Those folders contain all the output of one run of a simulation, and need to be labeled `out_<stimulus_speed>`.
You won't have to create those folders manually, if you use the script `cp_non_GUI_wrapper.py` it will create the `out_<stimulus_speed>` folders automatically. All you need for that script is a `template` folder that contains information on the stimulus and the neural circuit inside the `lambda<wavelength>deg` folders.
Before running the `cp_non_GUI_wrapper.py` your folder containing the data should look like this:
```
top-level folder
|
|-- lambda30deg
|   |
|   \-- template
|       |
|   	|-- circuit_object.pkl
|   	|-- surroundings_object.pkl
|   	|-- components.txt
|   	\-- sensors.txt
|
|-- lambda40deg
|   |
|   \-- template
|       |
|   	|-- circuit_object.pkl
|   	|-- surroundings_object.pkl
|   	|-- components.txt
|   	\-- sensors.txt
...
```
After running `cp_non_GUI_wrapper.py`, the data should have been generated and your folder should
look like this:
```
top-level folder
|
|-- lambda30deg
|   |
|   |-- template
|   |-- out_0
|   |	|
|   |	|-- intensities.npy
|   |	|-- neurons.npy
|   |	|-- sensors.npy
|   |	|-- time.npy
|   |	\-- values.pkl
|   |
|   |-- out_-0.015
|   |	|
|   |	...
|   ...
|       
|-- lambda40deg
|   |
|   |-- template
|   |-- out_0
|   |	|
|   |	|-- intensities.npy
|   |	|-- neurons.npy
|   |	|-- sensors.npy
|   |	|-- time.npy
|   |	\-- values.pkl
|   |
|   |-- out_-0.015
|   |	|
|   |	...
|   ...
...
```
To get the initial folder structure, you can either download it from zenodo ... STILL NEED TO UPLOAD ... or use the docker image ... PUT TOGETHER SOME DOCKER IMAGE
If you downloaded the template folders from zenodo and want to run the simulations on your machine, start `cp_non_GUI_wrapper.py` with the following arguments:
```
$ cp_non_GUI_wrapper.py path/to/data/folder/lambda30deg/ "[-1.0, -0.8, -0.7, -0.6, -0.5, -0.4, -0.35, -0.3, -0.25, -0.2, -0.15, -0.125, -0.1, -0.075, -0.06, -0.045, -0.03, -0.015, 0, 0.015, 0.03, 0.045, 0.06, 0.075, 0.1, 0.125, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0]" -n 4 --neurons-by-labels "['HS']" --sensors "[0, 1]"
```
The list of float values are the relative movement speeds of the stimulus (-1.0 would make the grating move to the left and rotate for 360 degree per second). There will be one simulation run for each speed value in the list, which means this call should run 37 simulations. Via the option `-n` you can specify how many simulations should run in parallel (each individual simulation is not parallelized, so you can put the number to as many cores you have, or maybe one less to keep your computer from becoming unresponsive). Via the `--neurons-by-labels` and `--sensors` options you can specify of which neuron types and of which sensors (by indices) you want to save the data. If you don't change this, the data of the HS cell and of both sensors will be saved to your disk. To produce the plots, storing only the data of the HS cell (the name HS cell does not really make sense here, it is used to sum up the inputs of the T4/T5 cells of the two columns in this set-up, however) is enough, so you could remove the `--sensors` option and its argument to save some space.  
Since the simulations will take some time, I recommend using tmux or similar tools, that will keep the simulations running even if you log out. You could also consider to chunk the list of stimulus speeds into several parts to run only a few simulations with one command.  
The data will be put into the `out_<stimulus-speed>` folders under the `lambda30deg` folder as described above. You need to repeat this call to `cp_non_GUI_wrapper.py` for the folders `lambda40deg`, `lambda60deg` and `lambda90deg`.

#### Plot the data

Adjust the `path_prefix` variable in the script `tuning_curve_EMD.py` and run it. This should produce the desired plot. You might need to zoom in a bit to see the exact same excerpt of the plots shown in the publication.


## Plots in **figure 5** - Tuning curve HSE

#### Generating the data
**BEWARE: This will roughly produce 13 GB of data and run for several days, depending on your machine's speed/number of cores.**  
  
The steps to reproduce data for these plots are mostly the same as those in the section above for the tuning curve of a single EMD. You will need different templates, however, and since there will be a few hundred times the number of columns used, the simulation time will be increased by a factor of a few hundred. If you are not running this on any cluster or remote machine, you should use a computer that you can occupy with computations for several days.  
If you downloaded the templates from zenodo ... TODO! ... you find the templates in the folder `tuning_curve_HSE`. Run the simulations in the same fashion as above using `cp_non_GUI_wrapper.py`. 

#### Plot the data

Adjust the `path_prefix` variable in the script `tuning_curve_HS.py` and run it. This should produce the desired plot. You might need to zoom in a bit to see the exact same excerpt of the plots shown in the publication.