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
accp_angle_H = accp_angle['accpBH']
accp_angle_V = accp_angle['accpBV']

accp_angle_H[:,0] = accp_angle_H[:, 0]*360/2./np.pi
accp_angle_V[:,0] = accp_angle_V[:, 0]*360/2./np.pi



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
## Looks like 'sphere_coordinates' are not really sphere coordinates,
# even though they are of shape (X,3). -> The third column is all 1.
# But first two columns seem to hold (phi, theta) pairs for spheric coordinates
# by the look of it (set plot_wo_last_column = True to show plot on running
# this script). However, angles for phi range from almost -2*pi to +2*pi.
# I will just divide by two for now .........
#sphere_coords_spheric=transform_sphere_surface(sphere_coords)
sphere_coords_spheric = sphere_coords[:,:2]
sphere_coords_spheric[:,0] /= 2.
## Furthermore, I want theta to range from 0 to pi rather than -pi/2 to pi/2
# --> shift by +pi/2
sphere_coords_spheric[:,1] += np.pi/2

coords_shape = sphere_coords.shape

gauss_coeffs_fit_H=optimize.curve_fit(gauss,accp_angle_H[:,0],accp_angle_H[:,1])
gauss_coeffs_fit_V=optimize.curve_fit(gauss,accp_angle_V[:,0],accp_angle_V[:,1])

gauss_sigma_from_literature = np.array([2.5,2.7])/2. # First value is for horizontal direction,
                                                  # second for vertical direction.
                                                  # This is sigma in degree.

print((gauss_coeffs_fit_H[0], gauss_coeffs_fit_V[0], gauss_sigma_from_literature))



if __name__=="__main__":

    save = False

    if save:
    
        np.save(here+'/bee_sphere_coords_spheric.npy',sphere_coords_spheric)
        np.save(here+'/bee_gauss_coeffs.npy',gauss_sigma_from_literature)

    ## set this to True if you want to see different options for acceptance angles visualized.
    plot = False

    import matplotlib.pyplot as plt
    
    if plot:
        f,ax = plt.subplots(1,1)
        ax.plot(accp_angle_H[:,0],accp_angle_H[:,1], label = "from file H")
        x = np.arange(-10,10,0.1)
        ax.plot(x, gauss(x,gauss_coeffs_fit_H[0]), label = "fit H")
        ax.plot(x, gauss(x, gauss_sigma_from_literature[0]), label = "literature H")
        ax.legend()

        f2,ax2 = plt.subplots(1,1)
        ax2.plot(accp_angle_V[:,0],accp_angle_V[:,1], label = "from file V")
        x = np.arange(-10,10,0.1)
        ax2.plot(x, gauss(x,gauss_coeffs_fit_V[0]), label = "fit V")
        ax2.plot(x, gauss(x, gauss_sigma_from_literature[1]), label = "literature V")
        ax2.legend()

        ## Droso for comparison
        ax.plot(accp_angle['accpAngle'][:,0],accp_angle['accpAngle'][:,1])
        ax2.plot(accp_angle['accpAngle'][:,0],accp_angle['accpAngle'][:,1])
        
        
        f.show()
        f2.show()

    def test_sphere_coords():
        from mpl_toolkits.mplot3d import Axes3D

        f=plt.figure()
        ax=f.gca(projection='3d')

        ax.plot(sphere_coords[:coords_shape[0]/2,0],sphere_coords[:coords_shape[0]/2,1],sphere_coords[:coords_shape[0]/2,2],ls='',marker='x',mec="red",label="left")
        ax.plot(sphere_coords[coords_shape[0]/2:,0],sphere_coords[coords_shape[0]/2:,1],sphere_coords[coords_shape[0]/2:,2],ls='',marker='x',mec="green",label="right")


        #for ticklbl in ax.get_xticklabels()+ax.get_yticklabels()+ax.get_zticklabels():
        #ticklbl.set_visible(False)

        ax.legend()

        f.show()

        return f,ax


    def test_spheric_coords():

        f,ax=plt.subplots()
        ax.plot(sphere_coords_spheric[:coords_shape[0]/2,0],sphere_coords_spheric[:coords_shape[0]/2,1],ls='',marker='x',mec='red')
        ax.plot(sphere_coords_spheric[coords_shape[0]/2:,0],sphere_coords_spheric[coords_shape[0]/2:,1],ls='',marker='x',mec='green')
        #ax.vlines([-np.pi,np.pi],0,np.pi,linestyles='solid',lw=5,color='black')
        #ax.hlines([0,np.pi],-np.pi,np.pi,linestyles='solid',lw=5,color='black')
        ax.grid()
        ax.invert_yaxis()
        f.show()

        return f,ax

    
    plot_sphere = False
    plot_spheric = True
    plot_wo_last_column = True
    if plot_sphere:
        f_sphere,ax_sphere = test_sphere_coords()
    if plot_spheric:
        f_spheric,ax_spheric = test_spheric_coords()
    if plot_wo_last_column:
        f,ax = plt.subplots(1,1)
        ax.plot(sphere_coords[:coords_shape[0]/2,0],sphere_coords[:coords_shape[0]/2,1],ls='',marker='x',mec="red",label="right")
        ax.plot(sphere_coords[coords_shape[0]/2:,0],sphere_coords[coords_shape[0]/2:,1],ls='',marker='x',mec="green",label="left")
        ax.grid()
        ax.legend()
        f.show()
        
