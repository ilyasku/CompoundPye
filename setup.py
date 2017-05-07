"""
Run this to install.
Modified from https://wiki.python.org/moin/Distutils/Tutorial.
"""

from setuptools import setup

setup(name = "CompoundPye",
      version = "0.95",
      description = "Modelling and simulation framework for neural nets of compound eyes.",
      author = "Ilyas Kuhlemann",
      author_email = "ilyasp.ku@gmail.com",
      url = "https://github.com/ilyasku/CompoundPye",
      #Name the folder where your packages live:
      #(If you have other packages (dirs) or modules (py files) then
      #put them into the package directory - they will be found 
      #recursively.)
      packages = ['CompoundPye',
                  'CompoundPye.Analyzer',
                  'CompoundPye.Circuits',
                  'CompoundPye.Components',
                  'CompoundPye.Components.Connections',
                  'CompoundPye.Graph',
                  'CompoundPye.GUI',
                  'CompoundPye.OmmatidialMap',
                  'CompoundPye.Parser',
                  'CompoundPye.Sensors',
                  'CompoundPye.Surroundings',
                  'CompoundPye.Surroundings.Stimuli'],
      package_data={'': ['*.mat', '*.pkl', '*.npy']},
      scripts=['executables/cp_GUI.py',
               'executables/cp_non_GUI_wrapper.py',
               'executables/cp_analyze_set_of_simulations.py',
               'executables/cp_analyze_single_simulation.py',
               'executables/cp_replace_T4_T5_inhibitory_with_LPis.py',
               'executables/cp_get_circuit_info.py'],
      long_description = """Modelling and simulation framework for neural networks of compound eyes.""" ,
      license="Creative Commons Attribution-ShareAlike 4.0 International License",
      install_requires=['numpy', 'scipy', 'matplotlib', 'networkx'],
      zip_safe=False
) 
