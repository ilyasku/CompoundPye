"""
Run this to install.
Modified from https://wiki.python.org/moin/Distutils/Tutorial.
"""

from setuptools import setup

setup(name = "CompoundPye",
      version = "0.94",
      description = "Modelling and simulation framework for neural nets of compound eyes.",
      author = "Ilyas Kuhlemann",
      author_email = "ilyasp.ku@gmail.com",
      url = "https://github.com/ilyasku/CompoundPye",
      #Name the folder where your packages live:
      #(If you have other packages (dirs) or modules (py files) then
      #put them into the package directory - they will be found 
      #recursively.)
      packages = ['CompoundPye',
                  'CompoundPye.executables',
                  'CompoundPye.src',
                  'CompoundPye.src.Analyzer',
                  'CompoundPye.src.Circuits',
                  'CompoundPye.src.Components',
                  'CompoundPye.src.Components.Connections',
                  'CompoundPye.src.ErrorHandling',
                  'CompoundPye.src.Graph',
                  'CompoundPye.src.GUI',
                  'CompoundPye.src.OmmatidialMap',
                  'CompoundPye.src.Parser',
                  'CompoundPye.src.Sensors',
                  'CompoundPye.src.Surroundings',
                  'CompoundPye.src.Surroundings.Stimuli'],
      package_data={'': ['*.mat', '*.pkl', '*.npy']},
      scripts=['CompoundPye/executables/cp_GUI.py',
               'CompoundPye/executables/cp_non_GUI_wrapper.py',
               'CompoundPye/executables/cp_analyze_set_of_simulations.py',
               'CompoundPye/executables/cp_analyze_single_simulation.py',
               'CompoundPye/executables/cp_replace_T4_T5_inhibitory_with_LPis.py',
               'CompoundPye/executables/cp_get_circuit_info.py'],
      long_description = """Modelling and simulation framework for neural networks of compound eyes.""" ,
      license="Creative Commons Attribution-ShareAlike 4.0 International License",
      install_requires=['numpy', 'scipy', 'matplotlib', 'networkx'],
      zip_safe=False
) 
