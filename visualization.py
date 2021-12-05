from openpiv import tools

import numpy as np
import matplotlib.pyplot as plt

tools.display_vector_field('result/CC_F005_wValidation/B00019_%05d.txt', on_img=True,
                                          image_name='dataset/Transformed_F005/B00019.tif', 
                                          window_size=16, scaling_factor=1, width=0.005, scale=80)

# tools.display_vector_field('dataset/MS_Images_F005/results/B00025.txt', on_img=True,
#                                           image_name='dataset/Transformed_F005/B00025.tif', 
#                                           window_size=16, scaling_factor=1, width=0.005, scale=80)