from openpiv import tools

import numpy as np
import matplotlib.pyplot as plt

tools.display_vector_field('dataset/PIV_F005/B00497_%05d.txt', on_img=True,
                                          image_name='dataset/Transformed_F005/B00497.tif', 
                                          window_size=16, scaling_factor=1, width=0.005, scale=80)