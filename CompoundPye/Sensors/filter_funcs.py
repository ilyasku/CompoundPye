## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 21.10.14

"""
@package CompoundPye.src.Sensors.filter_funcs
Contains filter functions, creating input filters that will be multiplied with an array of input intensities that a sensor 'observes'.

Currently contains only one- and two-dimensional gaussian filter. 
"""


import numpy as np



def two_dim_gauss(cut_off,px,rel_sigma,amplitude=1,search_step=10):
    """
    Creates a two-dimensional gaussian filter-array.
    
    The size of the array is intrinsically defined by the parameter cut_off. cut_off is the lowest relative value that is still to be included in the filter-array, looking at each direction individually.
    For example, if cut_off is 0.1, the filter-array stretches in x-direction up to a value x_i, for which exp(-x_i^2/2/sigma_x^2)>0.1, while exp(-x_(i+1)^2/2/sigma_x^2)<=0.1.  
    @param cut_off Sets the relative value that is still to be included in the array; defines filter-array size intrinsically.
    @param sigma List or array of two sigma values, one for each input dimension.
    @param amplitude Amplitude of the gaussian function at (x,y)=(0,0).
    @param search_step One can increase or decrease computational efficiency by changing the search_step; never tested how well this works, though.
    @return Two-dimensional filter-array.
    """

    sigma=rel_sigma*px

    r=[]
    for i in range(0,2):
        near=False
        x_i=0
        while not near:
            value=amplitude*np.exp(-x_i**2/2./sigma[i]**2)
            if value>cut_off:
                x_i+=search_step
            else:
                near=True
        found=False
        while not found:
            x_i-=1
            value=amplitude*np.exp(-x_i**2/2./sigma[i]**2)
            if value>cut_off:
                found=True
                r.append(x_i)
            else:
                pass
            
            
    filter=np.ones(2*np.array(r)+[1,1])*amplitude
    gauss0=np.exp(-np.arange(-r[0],r[0]+1)**2/2./sigma[0]**2)
    gauss1=np.exp(-np.arange(-r[1],r[1]+1)**2/2./sigma[1]**2)
    gauss=[gauss0,gauss1]
    
    for m in range(0,filter.shape[0]):
        filter[m,:]=filter[m,:]*gauss1
    for n in range(0,filter.shape[1]):
        filter[:,n]=filter[:,n]*gauss0

    return filter
            
    
def one_dim_gauss(cut_off,px,rel_sigma,amplitude=1,search_step=10):
    """
    Creates a one-dimensional gaussian filter-array.
    
    The size of the array is intrinsically defined by the parameter cut_off. cut_off is the lowest relative value that is still to be included in the filter-array.
    For example, if cut_off is 0.1, the filter-array stretches up to a value i, for which exp(-i^2/2/sigma^2)>0.1, while exp(-(i+1)^2/2/sigma^2)<=0.1.  
    @param cut_off Sets the relative value that is still to be included in the array; defines filter-array size intrinsically.
    @param sigma Defines width of the gaussian function..
    @param amplitude Amplitude of the gaussian function at postition i=0.
    @param search_step One can increase or decrease computational efficiency by changing the search_step; never tested how well this works, though.
    @return One-dimensional filter-array.
    """
    sigma=rel_sigma*px

    near=False
    x_i=0
    while not near:
        value=amplitude*np.exp(-x_i**2/2./sigma**2)
        if value>cut_off:
            x_i+=search_step
        else:
            near=True
    found=False
    while not found:
        x_i-=1
        value=amplitude*np.exp(-x_i**2/2./sigma**2)
        if value>cut_off:
            found=True
            r=x_i
        else:
            pass
    print(r)
    gauss=np.exp(-np.arange(-r,r+1)**2/2./sigma**2)
    #print gauss
    filter=np.ones(2*r+1)*amplitude*gauss
    #print filter
    
    return filter
    
def pixel_two_dim(dummy1,dummy2):
    return np.ones((1,1))

def pixel_one_dim(dummy1,dummy2):
    return np.ones(1)
