import os, os.path, sys, re

from openpiv import tools, pyprocess, validation, filters, tools
import numpy as np

def process_frames(frame_a, frame_b):
    winsize = 16 #16 * 16 interrogation window
    overlap = 12 #75% Overlap
    dt = 1 #3000fps

    u0, v0, sig2noise = pyprocess.extended_search_area_piv(
        frame_a.astype(np.int32), frame_b.astype(np.int32), 
        window_size=winsize, overlap=overlap, dt=dt, sig2noise_method='peak2peak')

    #Coordinates for further processing
    x, y = pyprocess.get_coordinates(
        image_size=frame_a.shape, search_area_size=winsize, overlap=overlap)

    #Remove value with low sig2noise ratio
    u1, v1, mask = validation.sig2noise_val(u0, v0, sig2noise, threshold = 1.05) 

    u2, v2 = filters.replace_outliers(u1, v1, method='localmean', max_iter=5,
        kernel_size=3)

    #0,0 shall be bottom left, positive rotation rate is counterclockwise
    x, y, u3, v3 = tools.transform_coordinates(x, y, u2, v2)

    #Return Coordinates, Velocity and Mask in px/dt
    return x, y, u3, v3, mask

#Folder Direcory of Dataset
file_directory = sys.argv[1]
destination = sys.argv[2]

if not os.path.exists(destination):
    os.mkdir(destination)

initalize = 0
frame_a = None
frame_b = None

for filename in sorted(os.listdir(file_directory)):
    if filename.endswith(".tif"):
        if initalize == 0:
            frame_a = tools.imread(os.path.join(file_directory, filename))
            initalize += 1
            continue
        elif initalize == 1:
            frame_b = tools.imread(os.path.join(file_directory, filename))
            initalize += 1
        else:
            frame_a = frame_b
            frame_b = tools.imread(os.path.join(file_directory, filename))

        #Get Result
        x, y, u3, v3, mask = process_frames(frame_a, frame_b)

        #Save Name
        save_file = re.findall(r"[\S]+\.", filename)[0] + "txt"
        
        #Save Frame
        tools.save(x, y, u3, v3, mask, os.path.join(destination, save_file))