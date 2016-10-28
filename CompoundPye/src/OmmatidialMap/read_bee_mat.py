##@author Ilyas Kuhlemann
#@contact ilyasp.ku@gmail.com
#@date 28.10.16 

"""
@package CompoundPye.src.OmmatidialMap.read_bee_mat
File to read Apis' ommatidia coordinates and acceptance angles from .m-files in this folder. 
"""

import scipy.io as io
from scipy import optimize
import numpy as np

import os
here=os.path.dirname(os.path.abspath(__file__))


# load gauss shaped acceptance curve
accp_angle = io.loadmat(here+"/accpAngle.mat")
# -> unlike those for droso, the data for bees is in rad.
accp_angle_H = accp_angle['accpBH']*360/2./np.pi
accp_angle_V = accp_angle['accpBV']*360/2./np.pi


def gauss(x,sigma):
    mu=0
    A=1
    return A*np.exp(-(x-mu)**2/(2*sigma**2))


def transform_sphere_surface(cartesian_coords):
    spheric_coords=np.zeros((cartesian_coords.shape[0],2))
    spheric_coords[:,1]=np.arccos(cartesian_coords[:,2])
    spheric_coords[:,0]=np.arctan(cartesian_coords[:,1]/cartesian_coords[:,0])
    negative=np.where(cartesian_coords[:,0]<0)[0]
    s=np.sign(cartesian_coords[negative,1])
    spheric_coords[negative,0]=s*np.pi+spheric_coords[negative,0]
    # to flip left eye from [0,pi] to [-pi,0], and vice versa for the right eye
    spheric_coords[:,0]=spheric_coords[:,0]*-1

    return spheric_coords

sphere_coords=io.loadmat(here+"/SphereCoordB.mat")["sphCoordB"]
sphere_coords_spheric=transform_sphere_surface(sphere_coords)

gauss_coeffs_fit_H=optimize.curve_fit(gauss,accp_angle_H[:,0],accp_angle_H[:,1])
gauss_coeffs_fit_V=optimize.curve_fit(gauss,accp_angle_V[:,0],accp_angle_V[:,1])

gauss_sigma_from_literature = np.array([2.5,2.7]) # First value is for horizontal direction,
                                                  # second for vertical direction.
                                                  # This is sigma in degree.

print(gauss_coeffs_fit[0], gauss_sigma_from_literature)

if __name__=="__main__":
    #np.save(here+'/bee_sphere_coords_spheric.npy',sphere_coords_spheric)
    #np.save(here+'/bee_gauss_coeffs.npy',gauss_coeffs_fit)

    plot = True

    if plot:
        import matplotlib.pyplot as plt
        f,ax = plt.subplots(1,1)
        ax.plot()
