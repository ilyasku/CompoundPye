CompoundPye is a framework designed for easy modelling and simulations of neural networks of arthropods' compound eyes.
Feedback is very welcome, since this is my first larger software project. Besides bug reports and questions, please point out 
if I missed any conventions I should follow to make this code more easy usable by others.
Everyone is invited to contribute to, use, and/or redistribute CompoundPye. I would license it under the MIT license, but I want to include models with full parameter sets at some point as well. Everyone building a model using CompoundPye should get the credit for that, as they would for publishing the data in other means of scientific communication. For this reason, I chose the Creative Commons license for now. I do not know if that is a clever choice. Any feedback on that issue is welcome as well!

## Install


CompundPye is written in Python (tested on Ubuntu 14.04 with Python 2.7.) and requires some other python packages (see below).
CompoundPye is registered with the Python Package Index (pypi.python.org), the most easy way to install is by using pip. 
On Ubuntu, open a command line and type:

> sudo pip install CompoundPye

If you downloaded the source (e.g. from github [FULL URL?]), open a command line, navigate to the top source directory
(it should contain the file "setup.py"), and type:

> sudo python setup.py install

## Requirements 

* numpy (tested: 1.9.2),
* PyQt4,
* networkx (tested: 1.10),
* cv2 (Python's openCV interface; optional for video stimuli).

## Quickstart

A good starting point is CompoundPye's GUI, run it using python in the command line:

> cp_GUI.py

@TODO ADD TUTORIAL ON GITHUB
