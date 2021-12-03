import sys, os, glob, re
from openpiv import tools, pyprocess, preprocess, validation, filters
import numpy as np


def func( args ):
    """A function to process each image pair."""

    # this line is REQUIRED for multiprocessing to work
    # always use it in your custom function

    file_a, file_b, counter = args
    
    print(file_a + file_b + str(counter))

    filepath, filename = os.path.split(file_a)
    filedrive, filepath = os.path.splitdrive(filepath)
    filename = os.path.splitext(filename)
    filepath = os.path.join('d:',filepath)
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    filename = os.path.join(filepath,filename[0])
    
    # print filepath

    # typical parameters:
    window_size = 16 #pixels
    overlap = 12 # pixels

    # Read the files
    im_a  = tools.imread( file_a )
    im_b  = tools.imread( file_b )

	# Process image and see the OpenPIV result:

	# process again with the masked images, for comparison# process once with the original images
    u, v, sig2noise = pyprocess.extended_search_area_piv(
														   im_a.astype(np.int32) , im_b.astype(np.int32), 
														   window_size = window_size,
														   overlap = overlap, 
														   dt=1,  
														   sig2noise_method = 'peak2peak')
    x, y = pyprocess.get_coordinates( image_size = im_a.shape, search_area_size = window_size, overlap = overlap )
    u, v, mask = validation.sig2noise_val( u, v, sig2noise, threshold = 1.05)
    u, v = filters.replace_outliers( u, v, method='localmean', max_iter = 5, kernel_size = 3)
	
	# save to a file using the original filename and the counter
    tools.save(x, y, u, v, mask, os.path.join(rootdir, (filename+'_%05d.txt')), fmt='%8.7f', delimiter='\t')
	# openpiv.tools.save(x, y, u, v, mask, 'test_masked.txt', fmt='%9.6f', delimiter='\t')
	# openpiv.tools.display_vector_field('test_masked.txt', scale=50, width=0.002)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("rootdir", help="name of the root directory",
                    type=str)
    args = parser.parse_args()
    print(args.rootdir, os.path.isdir(args.rootdir))
    
          
    rootdir = args.rootdir
    filepattern = r'*.tif'
    for root, dirnames, filenames in os.walk(rootdir):
        if dirnames == []: # lowest directory level
            print(root)
            task = tools.Multiprocesser( data_dir = root, pattern_a = filepattern, pattern_b = None)
            task.run( func = func, n_cpus = 5 ) #Control your own CPU Core Allocation