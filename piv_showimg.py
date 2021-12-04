from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def imadjust(x,a,b,c,d,gamma=1):
    # Similar to imadjust in MATLAB.
    # Converts an image range from [a,b] to [c,d].
    # The Equation of a line can be used for this transformation:
    #   y=((d-c)/(b-a))*(x-a)+c
    # However, it is better to use a more generalized equation:
    #   y=((x-a)/(b-a))^gamma*(d-c)+c
    # If gamma is equal to 1, then the line equation is used.
    # When gamma is not equal to 1, then the transformation is not linear.

    y = (((x - a) / (b - a)) ** gamma) * (d - c) + c
    return y

fname1 = 'C:/Users/Nicole Lui/Desktop/MS_Images_B013/B00080.tif'
image = Image.open(fname1)
arr = np.asarray(image)
arr2=imadjust(arr,arr.min(),arr.max(),0,1)


fig = plt.figure()
fig.suptitle('image')
plt.imshow(arr2)
plt.show()
