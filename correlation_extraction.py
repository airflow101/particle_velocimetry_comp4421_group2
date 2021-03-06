from datetime import time
import os, os.path, sys, re

from numpy import empty, float64
import numpy as np
import pandas as pd

from functools import lru_cache

@lru_cache(maxsize=32)
def read_hdr_ms_table(file_hdr, file_ms):
    #Read .dat file
    df_hdr = pd.read_csv(file_hdr, skiprows=3, sep="\s+",
    names=["X", "Y", "Vx", "Vy", "Vz", "flag"])
    
    #Only filter for valid flag and remove column
    df_hdr = df_hdr[df_hdr.flag != 0]
    df_hdr = df_hdr.drop(['Vz', 'flag'], 1)

    #Remove Pixel that is not mod of 4 (search window pixel)
    modulo = df_hdr[(df_hdr["X"] % 4 != 0) | (df_hdr["Y"] % 4 != 0)].index
    df_hdr.drop(modulo , inplace=True)

    #Valid Pixels
    x_min = df_hdr['X'].min()
    y_min = df_hdr['Y'].min()
    x_max = df_hdr['X'].max()
    y_max = df_hdr['Y'].max()

    #Read .txt output of PIV
    df_ms = pd.read_csv(file_ms, skiprows=1, sep="\t",
    names=["x", "y", "u", "v", "mask"])

    #Convert x and y to int
    df_ms = df_ms.astype({"x": int, "y": int, "u":float64, "v":float64})

    #Remove pixel not in HDR
    index_x = df_ms[(df_ms["x"] < x_min) | (df_ms["x"] > x_max)].index
    df_ms.drop(index_x , inplace=True)
    index_y = df_ms[(df_ms["y"] < y_min) | (df_ms["y"] > y_max)].index
    df_ms.drop(index_y , inplace=True)

    #Sort Column
    df_hdr = df_hdr.sort_values(by=['X', 'Y'])
    df_ms = df_ms.sort_values(by=['x', 'y'])

    #Combine
    df_hdr = df_hdr.rename(columns={'X': 'x', 'Y': 'y'})
    df_combine = pd.merge(df_hdr, df_ms, on=['x', 'y'])
    #Fill with Linear Interpolation For NaN
    df_combine = df_combine.interpolate(method='linear', limit_direction='forward', axis=0)
    
    return df_combine

#Folder Direcory of Dataset
file_directory_hdr = sys.argv[1]
file_directory_ms = sys.argv[2]

ms_files = os.listdir(file_directory_ms)

time_series_data = {} #Store DF

for filename in sorted(os.listdir(file_directory_hdr)):
    if filename.endswith(".dat"):
        naming_sequence = re.findall(r"[\w]+", filename)[0]
        
        #Get Matching Name
        r = re.compile(r"%s[\S]+\.txt" % naming_sequence)
        ms_lists = list(filter(r.match, ms_files))

        #Final Time Iteration
        if(len(ms_lists) == 0):
            continue

        combine_table = read_hdr_ms_table(os.path.join(file_directory_hdr, filename),
        os.path.join(file_directory_ms, ms_lists[0]))

        time_series_data[naming_sequence] = combine_table

combined_data = np.empty((0, 4))

for key, df_combined in time_series_data.items():
    time_name = key
    df_combined = df_combined.set_index(["x", "y"])
    ms_Vx = df_combined.loc[(320, 220)]["u"]
    ms_Vy = df_combined.loc[(320, 220)]["v"]
    hdr_Vx = df_combined.loc[(320, 220)]["Vx"]
    hdr_Vy = df_combined.loc[(320, 220)]["Vy"]
    row_data = np.array([[ms_Vx, ms_Vy, hdr_Vx, hdr_Vy]])
    combined_data = np.append(combined_data, row_data, axis = 0)

df_time_series = pd.DataFrame(combined_data, columns = ["ms_Vx", "ms_Vy", "hdr_Vx", "hdr_Vy"])
df_time_series["ms_res"] = np.linalg.norm(df_time_series[["ms_Vx","ms_Vy"]].values,axis=1)
df_time_series["hdr_res"] = np.linalg.norm(df_time_series[["hdr_Vx","hdr_Vy"]].values,axis=1)
df_time_series["d_Vx"] = df_time_series["ms_Vx"] - df_time_series["hdr_Vx"]
df_time_series["d_Vy"] = df_time_series["ms_Vy"] - df_time_series["hdr_Vy"]
df_time_series["d_res"] = df_time_series["ms_res"] - df_time_series["hdr_res"]
df_time_series["d_relative_Vx"] = df_time_series["d_Vx"] * 100 / df_time_series["hdr_Vx"]
df_time_series["d_relative_Vy"] = df_time_series["d_Vy"] * 100 / df_time_series["hdr_Vy"]
df_time_series["d_relative_res"] = df_time_series["d_res"] * 100 / df_time_series["hdr_res"]

df_time_series[["d_Vx", "d_Vy", "d_res", "d_relative_Vx", "d_relative_Vy", "d_relative_res"]].mean().to_csv(
    "results_mean.csv", sep="\t", header=False)

df_time_series.to_csv("results_aggregate.csv", index=False, sep="\t", float_format='%g')
(df_time_series.corr()).to_csv("results_correlation.csv", sep="\t", float_format='%g')

# np.savetxt("result.csv", combined_data, delimiter="\t", header="ms_Vx, ms_Vy, hdr_Vx, hdr_Vy")
