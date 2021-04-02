import pandas as pd
from legacy.read_pics import get_pics_from_file
from legacy.data_clean import detect_outliers

def generate_df(pics, label):
    df =  pd.DataFrame.from_records(pics)
    df['label'] = label
    return df

def generate_dataset_dataframe(alphanum, touchesspe, clean_data=False):
    df_1 = pd.DataFrame()
    df_cleaned = pd.DataFrame()
    for c in alphanum:
        pics, info = get_pics_from_file("../input/Hackaton/data/pics_" + c + ".bin")
        df_test = generate_df(pics, c)
        if clean_data:
            df_temp = detect_outliers(df_test)
            df_temp['label'] = c
            df_cleaned = df_cleaned.append(df_temp)
        df_1 = df_1.append(df_test)
        
    for c in touchesspe:
        pics, info = get_pics_from_file("../input/Hackaton/data/pics_" + c + ".bin")
        df_test = generate_df(pics, c)
        if clean_data:
            df_temp = detect_outliers(df_test)
            df_temp['label'] = c
            df_cleaned = df_cleaned.append(df_temp)
        df_1 = df_1.append(df_test)
    
    print("Loaded Dataframe")
    return df_1, df_cleaned