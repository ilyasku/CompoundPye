##@author Ilyas Kuhlemann
#@contact ilyasp.ku@gmail.com
#@date 08.10.15 

#last_update: 15.10.15

"""
@package CompoundPye.src.OmmatidialMap.read_droso
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


def write_sphere_coords_spheric_to_sensor_file_buffer(phi_range=[-np.pi,np.pi],theta_range=[0,np.pi], borders=0.0,eyes='both',fname_prefix=None):
    _eyes=np.array(['left']*699+['right']*699)
    if eyes=='both':
        photor_coords=sphere_coords_spheric
    elif eyes=='left':
        photor_coords=sphere_coords_spheric[:699,:]
        _eyes=_eyes[:699]
    elif eyes=='right':
        photor_coords=sphere_coords_spheric[699:,:]
        _eyes=_eyes[699:]

    exec('borders='+str(borders))

    borders_phi=(borders[0]*(phi_range[1]-phi_range[0]),borders[1]*(phi_range[1]-phi_range[0]))
    borders_theta=(borders[2]*(theta_range[1]-theta_range[0]),borders[3]*(theta_range[1]-theta_range[0]))

    where=np.where((photor_coords[:,0]>=phi_range[0]+borders_phi[0]) & (photor_coords[:,0] <=phi_range[1]-borders_phi[1]) & (photor_coords[:,1]>=theta_range[0]+borders_theta[0]) & (photor_coords[:,1]<=theta_range[1]-borders_theta[1]))[0]

    photor_coords=photor_coords[where,:]
    _eyes=_eyes[where]

    s='neighbours=x\n#x\ty\tname\tsensor-class\tsensor-parameters\tfilter-function\tfunction-parameters\tneighbourhood?\nsensors{\n'
    
    for i in range(photor_coords.shape[0]):
        x_i=float(photor_coords[i,0]-phi_range[0])/(phi_range[1]-phi_range[0])
        #y_i=float(photor_coords[i,1]-theta_range[0])/(theta_range[1]-theta_range[0])
        # need to convert: theta is increasing with decreasing height, so I need to flip values
        y_i=1-float(photor_coords[i,1]-theta_range[0])/(theta_range[1]-theta_range[0])
        coeffx=gauss_coeffs_fit[0]/180./((phi_range[1]-phi_range[0])/2./np.pi)
        coeffy=gauss_coeffs_fit[0]/180./((theta_range[1]-theta_range[0])/np.pi)
        s_i=str(x_i)+'\t'+str(y_i)+'\t'+'s_'+str(i)+'\tPhotoreceptor\t'+'-\t'+'gaussian\t['+str(coeffx[0])+','+str(coeffy[0])+']\t'+_eyes[i]+'\n'
        s=s+s_i
        
    s=s+'}'

    if fname_prefix==None:
        return s
    else:
        f=open(fname_prefix+'_phi_'+str(phi_range[0])+','+str(phi_range[1])+'_theta_'+str(theta_range[0])+','+str(theta_range[1])+'.txt','w')
        f.write(s)
        f.close()

def test_sphere_coords():
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    f=plt.figure()
    ax=f.gca(projection='3d')

    ax.plot(sphere_coords[:699,0],sphere_coords[:699,1],sphere_coords[:699,2],ls='',marker='x',mec="red",label="left")
    ax.plot(sphere_coords[699:,0],sphere_coords[699:,1],sphere_coords[699:,2],ls='',marker='x',mec="green",label="right")
    
    
    for ticklbl in ax.get_xticklabels()+ax.get_yticklabels()+ax.get_zticklabels():
        ticklbl.set_visible(False)
    
    ax.legend()

    f.show()

    return f,ax

def animate_sphere():
    """
    Function creating an animation video of ommatidial coordinates plotted in 3D.

    Actually does not create the video in the end. Something has to be wrong with the save-function.
    """
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import animation

    f=plt.figure()
    ax=f.gca(projection="3d")

    def init():
        ax.plot(sphere_coords[:699,0],sphere_coords[:699,1],sphere_coords[:699,2],ls='',marker='x',mec="red",label="left")
        ax.plot(sphere_coords[699:,0],sphere_coords[699:,1],sphere_coords[699:,2],ls='',marker='x',mec="green",label="right")
        ax.legend()
        #for ticklbl in ax.get_xticklabels()+ax.get_yticklabels()+ax.get_zticklabels():
            #ticklbl.set_visible(False)
        return []

    def animate(i):
        ax.view_init(elev=30.,azim=i)
        return []

    anim=animation.FuncAnimation(f,animate,init_func=init,frames=360,interval=20,blit=False)
    
    f.show()
    #anim.save('sphere_animation.mp4',fps=30,extra_args=['-vcodec','libx264'])


def test_spheric_coords():
    import matplotlib.pyplot as plt

    f,ax=plt.subplots()
    ax.plot(sphere_coords_spheric[:699,0],sphere_coords_spheric[:699,1],ls='',marker='x',mec='red')
    ax.plot(sphere_coords_spheric[699:,0],sphere_coords_spheric[699:,1],ls='',marker='x',mec='green')
    #ax.vlines([-np.pi,np.pi],0,np.pi,linestyles='solid',lw=5,color='black')
    #ax.hlines([0,np.pi],-np.pi,np.pi,linestyles='solid',lw=5,color='black')
    ax.invert_yaxis()
    f.show()

    return f,ax


def test_gauss_fit():
    import matplotlib.pyplot as plt
    
    f,ax=plt.subplots()
    x=np.arange(-15,15,0.01)
    
    ax.plot(accp_angle[:,0],accp_angle[:,1],label='data')
    ax.plot(x,gauss(x,*gauss_coeffs[0,:1]),label='with .mat params')
    #ax.plot(x,gauss(x,*gauss_coeffs_fit[0]),label='my fit')
    ax.plot(x,gauss(x,*gauss_coeffs_fit[0]),label='my fit')
    ax.legend()

    f.show()


