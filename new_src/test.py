alphanum = "abcdefghijklmnopqrstuvwxyz0123456789"
touchesspe = ["CTRL", "ENTER", "NOKEY", "SHIFT", "SPACE", "SUPPR"]

from legacy.prepare_data import generate_dataset_dataframe

df, df_cleaned = generate_dataset_dataframe(alphanum, touchesspe, False)

import pandas as pd
unique = df['label'].unique()
df_new = pd.DataFrame()
for v in unique:
    mean = df[df['label'] == v].mean()
    df_new[v] = mean
df_new

import seaborn as sn
import matplotlib.pyplot as plt
corrMatrix= df_new.corr()
sn.heatmap(corrMatrix, xticklabels=corrMatrix.columns, yticklabels=corrMatrix.columns)
plt.figure(1)
plt.show()