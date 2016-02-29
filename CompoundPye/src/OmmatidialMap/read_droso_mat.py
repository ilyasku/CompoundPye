##@author Ilyas Kuhlemann
#@contact ilyasp.ku@gmail.com
#@date 08.10.15 

#last_update: 29.02.16

"""
@package CompoundPye.src.OmmatidialMap.read_droso_mat
File to read Drosophila's ommatidia coordinates and acceptance angles from .m-files in this folder. 
"""

import scipy.io as io
import numpy as np
from scipy import optimize

#from CompoundPye.settings import path

import os
here=os.path.dirname(os.path.abspath(__file__))

# filter data, one-dimensional, from ~ -15 to 15, gauss shaped
#d_accpAngle=io.loadmat(path+"/OmmatidialMap/accpAngle.mat")
accp_angle=io.loadmat(here+"/accpAngle.mat")['accpAngle']

# gauss fit to that data?
#d_accpAngleGaussFit=io.loadmat(path+"/OmmatidialMap/accpAngleGaussFit.mat")
gauss_coeffs=io.loadmat(here+"/accpAngleGaussFit.mat")['Dcoeff']
## don't get what the coeffs mean, plotting accp_angle and a gauss with gauss_coeffs in any permutation 
# do not seem to work.
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

sphere_coords=io.loadmat(here+"/SphereCoord.mat")["SphereCoord"]
#sphere_coords=sphere_coords[:699]
sphere_coords_spheric=transform_sphere_surface(sphere_coords)

gauss_coeffs_fit=optimize.curve_fit(gauss,accp_angle[:,0],accp_angle[:,1])


if __name__=="__main__":
    np.save(here+'/droso_sphere_coords_spheric.npy',sphere_coords_spheric)
    np.save(here+'/droso_gauss_coeffs.npy',gauss_coeffs_fit)
