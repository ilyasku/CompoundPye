# How to reproduce the data of publication XY

## Plots in **figure 3** - T4 response to pseudo motion

Execute the script `T4_response_to_pseudo_motion.py`. This will generate the same plot as seen in the publication. Have a look into the script to see how the data is generated.

## Plots in **figure 4** - Tuning curve EMD

The plot script `tuning_curve_EMD.py` requires you to have the data of the EMD simulations in a folder with several subfolders.
There needs to be one subfolder for each grating size, named `lambda<wavelength>deg` (<wavelength> should be 30, 40, 50 and 60, which are the wavelengths I used for the plots).
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


Generate the data or copy it ... 

Adjust the `path_prefix` variable in the script `tuning_curve_EMD.py` and run it. This should produce the desired plot. Ignore the initial 15 seconds of the upper right plot before annealing (zoom into it starting at around 15 s to see the same slice as in figure 4 of the publication).