import cv2
import numpy as np

out_file='flicker_3Hz.avi'

t_end=12
flickr_freq=3
flickr_up=0.8
flickr_down=0.2


w=500
h=500
fps=flickr_freq*2

fourcc=cv2.VideoWriter_fourcc(*'HFYU')
writer=cv2.VideoWriter(out_file,fourcc,fps,(w,h),False)


#intensities=np.ones((w,h))*flickr_up

intensities_up=(np.ones((w,h))*flickr_up*255).astype(np.uint8)
intensities_down=(np.ones((w,h))*flickr_down*255).astype(np.uint8)


for i in range(flickr_freq*t_end):
    
    writer.write(intensities_up)
    writer.write(intensities_down)
