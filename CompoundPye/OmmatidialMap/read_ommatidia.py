##@author Ilyas Kuhlemann
#@contact ilyasp.ku@gmail.com
#@date 29.02.16

#last_update: 29.02.16

"""
@package CompoundPye.src.OmmatidialMap.read_droso
File to read Drosophila's ommatidia coordinates and acceptance angles from .npy-files in this folder. 
"""

import numpy as np

import os
here=os.path.dirname(os.path.abspath(__file__))

def write_sphere_coords_spheric_to_sensor_file_buffer(phi_range=[-np.pi,np.pi],theta_range=[0,np.pi], borders=0.0,eyes='both',fname_prefix=None, animal = 'droso'):

    sphere_coords_spheric=np.load(here+'/'+animal+'_sphere_coords_spheric.npy')
    gauss_coeffs_fit=np.load(here+'/'+animal+'_gauss_coeffs.npy')
    coords_shape = sphere_coords_spheric.shape

    print(("creating photoreceptors for %s" % animal))
    
    
    _eyes=np.array(['left']*(coords_shape[0]/2)+['right']*(coords_shape[0]/2))
    
    if eyes=='both':
        photor_coords=sphere_coords_spheric
    elif eyes=='left':
        photor_coords=sphere_coords_spheric[:coords_shape[0]/2,:]
        _eyes=_eyes[:coords_shape[0]/2]
    elif eyes=='right':
        photor_coords=sphere_coords_spheric[coords_shape[0]/2:,:]
        _eyes=_eyes[coords_shape[0]/2:]

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
        coeffy=gauss_coeffs_fit[1]/180./((theta_range[1]-theta_range[0])/np.pi)
        #print coeffx, coeffy
        s_i=str(x_i)+'\t'+str(y_i)+'\t'+'s_'+str(i)+'\tPhotoreceptor\t'+'-\t'+'gaussian\t['+str(coeffx)+','+str(coeffy)+']\t'+_eyes[i]+'\n'
        s=s+s_i
        
    s=s+'}'

    print(("Number of photoreceptors created: %i" % photor_coords.shape[0]))

    if fname_prefix==None:
        return s
    else:
        f=open(fname_prefix+'_phi_'+str(phi_range[0])+','+str(phi_range[1])+'_theta_'+str(theta_range[0])+','+str(theta_range[1])+'.txt','w')
        f.write(s)
        f.close()

'''
def test_sphere_coords():
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    f=plt.figure()
    ax=f.gca(projection='3d')

    ax.plot(sphere_coords[:coords_shape[0]/2,0],sphere_coords[:coords_shape[0]/2,1],sphere_coords[:699,2],ls='',marker='x',mec="red",label="left")
    ax.plot(sphere_coords[699:,0],sphere_coords[699:,1],sphere_coords[699:,2],ls='',marker='x',mec="green",label="right")
    
    
    for ticklbl in ax.get_xticklabels()+ax.get_yticklabels()+ax.get_zticklabels():
        ticklbl.set_visible(False)
    
    ax.legend()

    f.show()

    return f,ax
'''

'''
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
'''


def test_spheric_coords(animal = 'droso'):
    import matplotlib.pyplot as plt

    sphere_coords_spheric=np.load(here+'/'+animal+'_sphere_coords_spheric.npy')
    gauss_coeffs_fit=np.load(here+'/'+animal+'_gauss_coeffs.npy')
    coords_shape = sphere_coords_spheric.shape
    
    f,ax=plt.subplots()
    ax.plot(sphere_coords_spheric[:coords_shape[0]/2,0],sphere_coords_spheric[:coords_shape[0]/2,1],ls='',marker='x',mec='red')
    ax.plot(sphere_coords_spheric[coords_shape[0]/2:,0],sphere_coords_spheric[coords_shape[0]/2:,1],ls='',marker='x',mec='green')
    #ax.vlines([-np.pi,np.pi],0,np.pi,linestyles='solid',lw=5,color='black')
    #ax.hlines([0,np.pi],-np.pi,np.pi,linestyles='solid',lw=5,color='black')
    ax.invert_yaxis()
    f.show()

    return f,ax

'''
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
'''
