## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 14.11.14

"""
@package CompoundPye.src.Sensors.create_array
NOT USED SINCE v0.42!
Provides functions to create arrays of sensors
(e.g. a block of photoreceptors).
"""


from . import sensor
from . import photoreceptor
import numpy as np
import multiprocessing as mp

import sys
from CompoundPye.settings import *


def create_sensor_array(start, n, distance, filter='gaussian',
                        filter_params=[], filter_kw_params={'sigma': [5, 5]}):
    """
    Creates an array of sensors, and sets their receptive fields.

    The user needs to provide the starting point (center of first sensor's
    receptive field), the number of sensors and the distance between neighbors'
    receptive fields.
    @param start Starting coordinates of the block (position of the first
    sensor's receptive field in pixels).
    @param n Number of sensors (needs to be a list/array with two elements for
    2-dimensional surroundings).
    @param distance Distance in pixels between two neighboring sensors'
    receptive fields.
    @param filter Keyword to select a filter; options
    (only one at the moment...): gaussian
    @param filter_params List of parameters to be passed on to the filter
    function.
    @param filter_kw_params Dictionary containing keyword parameters to be
    passed on to the filter function.
    @return Array of Sensor-objects.
    """
    start.reverse()
    n.reverse()
    distance.reverse()

    if len(start) == 2:
        array = _create_2_dim_sensor_array(start, n, distance,
                                           filter, filter_params,
                                           filter_kw_params)
    else:
        array = _create_1_dim_sensor_array(start, n, distance,
                                           filter, filter_params,
                                           filter_kw_params)
    return array


def _create_2_dim_sensor_array(start, n, distance, filter,
                               filter_params, filter_kw_params):
    """
    Creates a two-dimensional array of sensors.
    @param start Starting coordinates of the block (in pixels).
    @param n Number of sensors (needs to be a list/array with two
    elements for 2-dimensional surroundings).
    @param distance Distance in pixels between two neighboring sensors.
    @param filter Keyword to select a filter; options
    (only one at the moment...): gaussian
    @param filter_params List of parameters to be passed on to the
    filter function.
    @param filter_kw_params Dictionary containing keyword parameters
    to be passed on to the filter function.
    @return Array of Sensor-objects.
    """
    start = np.array(start)
    distance = np.array(distance)
    array = []
    for i in range(0, n[0]):
        column = []
        for j in range(0, n[1]):
            new_sensor = sensor.Sensor()
            new_sensor.set_receptive_field(start + np.array([i, j])*distance,
                                           filter, filter_params,
                                           filter_kw_params)
            column.append(new_sensor)
        array.append(column)
    return np.array(array)


def _create_1_dim_sensor_array(start,n,distance,filter,filter_params,filter_kw_params):
    """
    Creates a one-dimensional array of sensors.
    
    @note NOT WORKING YET
    @param start Starting coordinates of the block (in pixels).
    @param n Number of sensors (needs to be a list/array with two elements for 2-dimensional surroundings).
    @param distance Distance in pixels between two neighboring sensors.
    @param filter Keyword to select a filter; options (only one at the moment...): gaussian
    @param filter_params List of parameters to be passed on to the filter function.
    @param filter_kw_params Dictionary containing keyword parameters to be passed on to the filter function.
    @return Array of Sensor-objects.
    """
    pass


def create_2_dim_photoreceptor_array(dt,start,n,distance,filter='gaussian',filter_params=[],filter_kw_params={'sigma':[5,5]}):
    """
    Creates a two-dimensional array of photoreceptors(sensors).
    @param dt Time step; necessary for updateing the photoreceptors.
    @param start Starting coordinates of the block (in pixels).
    @param n Number of sensors (needs to be a list/array with two elements for 2-dimensional surroundings).
    @param distance Distance in pixels between two neighboring sensors.
    @param filter Keyword to select a filter; options (only one at the moment...): gaussian
    @param filter_params List of parameters to be passed on to the filter function.
    @param filter_kw_params Dictionary containing keyword parameters to be passed on to the filter function.
    @return Array of Sensor-objects.
    """
    start.reverse()
    n.reverse()
    distance.reverse()
    
    
    start=np.array(start)
    distance=np.array(distance)
    array=[]
    #if n_processes==1:
    for i in range(0,n[0]):
        column=[]
        for j in range(0,n[1]):
            new_sensor=photoreceptor.Photoreceptor(dt)
            new_sensor.set_receptive_field(start+np.array([i,j])*distance,filter,filter_params,filter_kw_params)
            column.append(new_sensor)
        array.append(column)
    #else:
        #pool=mp.Pool(n_processes)
        #array=[pool.apply(_create_photoreceptor_column, args=(i,n[1],dt,start,distance,filter,filter_params,filter_kw_params)) for i in range(0,n[0])]
    return np.array(array)
'''
def _create_photoreceptor_column(i,n1,dt,start,distance,filter,filter_params,filter_kw_params):
    column=[]
    for j in range(0,n1):
        new_sensor=photoreceptor.Photoreceptor(dt)
        new_sensor.set_receptive_field(start+np.array([i,j])*distance,filter,filter_params,filter_kw_params)
        column.append(new_sensor)
    return column
'''     
