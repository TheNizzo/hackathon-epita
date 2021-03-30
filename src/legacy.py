import numpy as np
import pandas as pd

def mean_from_pic(pics):
    arr = np.zeros(len(pics[0]))
    for i in range(len(arr)):
        for pic in pics:
            arr[i] += pic[i]
        arr[i] /= len(pics)
    return arr

# mean_from_pic([[1, 2], [0, 1]])

def generate_df(pics, label):
    df =  pd.DataFrame.from_records(pics)
    df['label'] = label
    return df


        
     
