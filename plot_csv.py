import pandas as pd
import matplotlib.pyplot as plt

headers = ["ms_Vx", "ms_Vy", "hdr_Vx", "hdr_Vy"]

df = pd.read_csv('result.csv', names=headers, delimiter="\t")

ax = plt.gca()

df.plot(kind='line',y='ms_Vy',ax=ax)
df.plot(kind='line',y='hdr_Vy', color='red', ax=ax)


plt.show()