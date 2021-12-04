from openpiv import tools

import numpy as np
import matplotlib.pyplot as plt

tools.display_vector_field('result/PIV_F005/B00025_%05d.txt', on_img=True,
                                          image_name='dataset/Transformed_F005/B00025.tif', 
                                          window_size=16, scaling_factor=1, width=0.005, scale=80)

# tools.display_vector_field('dataset/MS_Images_F005/results/B00025.txt', on_img=True,
#                                           image_name='dataset/Transformed_F005/B00025.tif', 
#                                           window_size=16, scaling_factor=1, width=0.005, scale=80)