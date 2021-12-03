from numpy import float64
import pandas as pd

#Read .dat file
df = pd.read_csv('dataset/HDR_data_F005/B00497.dat', skiprows=3, sep="\s+",
names=["X", "Y", "Vx", "Vy", "Vz", "flag"])

#Only filter for valid flag and remove column
df = df[df.flag != 0]
df = df.drop(['Vz', 'flag'], 1)

#Remove Pixel that is not mod of 4 (search window pixel)
modulo = df[(df["X"] % 4 != 0) | (df["Y"] % 4 != 0)].index
df.drop(modulo , inplace=True)

#Valid Pixels
x_min = df['X'].min()
y_min = df['Y'].min()
x_max = df['X'].max()
y_max = df['Y'].max()

#Read .txt output of PIV
df_ms = pd.read_csv('dataset/PIV_F005/B00497_%05d.txt', skiprows=1, sep="\t",
names=["x", "y", "u", "v", "mask"])

#Convert x and y to int
df_ms = df_ms.astype({"x": int, "y": int, "u":float64, "v":float64})

#Remove pixel not in HDR
index_x = df_ms[(df_ms["x"] < x_min) | (df_ms["x"] > x_max)].index
df_ms.drop(index_x , inplace=True)
index_y = df_ms[(df_ms["y"] < y_min) | (df_ms["y"] > y_max)].index
df_ms.drop(index_y , inplace=True)

#Sort Column
df = df.sort_values(by=['X', 'Y'])
df_ms = df_ms.sort_values(by=['x', 'y'])

#Combine
df = df.rename(columns={'X': 'x', 'Y': 'y'})
df_combine = pd.merge(df, df_ms, on=['x', 'y'])

print(df_combine["x", "y"].corr())