# Particle Image Velocimetry Executable Codes
In this repository, we have uploaded several of the python scripts that we've used for our experiments
Images to be used should be in a folder without anything else inside it
The datasets used are as follows (keep in mind to download both the images as well as the HDR results):
1. B013 - Varying Particle Image http://piv.de/uncertainty/?page_id=46
2. B009: Seeding density > 0.1 ppp - http://piv.de/uncertainty/?p=64
3. F005 - Large Seeding Density http://piv.de/uncertainty/?p=62


- ```python cross_correlation.py FILE_DIR DEST``` is the command to run  ```cross_correlation.py``` with the dataset pointed by FILE_DIR with the results being saved to DEST
- ```python multiprocess_cross_correlation.py ROOTDIR ``` is the command to run the parallelized version of the above. ROOTDIR will be the folder that is walked to find the images dataset. The results will be saved to ROOTDIR as well.
- ```python correlation_extraction.py HDR_LOC MS_LOC``` is the command to calculate all the data into a single PANDAS dataframe which is then saved to ```results_aggregate.csv``` and ```results_correlation.csv```
- ```python piv_showimg.py``` is used to perform contrast stretching and show a TIFF image so that it can show in normal viewers instead of being black
- ```python plot_csv.py``` plots a file named ```results.csv```
- ```python visualization.py``` helper script for viewing a particular file
