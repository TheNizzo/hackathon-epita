import matplotlib.pyplot as plt
import pandas as pd

def detect_outliers(df: pd.DataFrame):
    df = df.drop('label', 1)
    plt.figure(1)
    for i in range(100):
        df.iloc[i].plot.line()
    
    df1 = pd.DataFrame()
    for column in df.columns:
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        IQR = q3-q1
        #print(df.describe())
        df1[column] = (df[column] < (q1 - 1.5 * IQR)) | (df[column] > (q3 + 1.5 * IQR))
    
    df = df[(df1 == True).sum(axis=1) <= 3]
    # import pdb; pdb.set_trace()
    return df
    # print(df.info())
    # print(df)
    # plt.figure(2)
    # plt.subplot(111)
    # for i in range(100):
    #     df.iloc[i].plot.line()
    # plt.show()
    #df1.to_csv('result6.csv')