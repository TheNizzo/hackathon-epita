from read_pics import get_pics_from_file
from legacy import mean_from_pic, generate_df
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

if __name__ == "__main__":
    alphanum = "abcdefghijklmnopqrstuvwxyz0123456789"
    touchesspe = ["CTRL", "ENTER", "NOKEY", "SHIFT", "SPACE", "SUPPR"]
    df = pd.DataFrame()
    for c in alphanum:
        pics, info = get_pics_from_file("../input/Hackaton/data/pics_" + c + ".bin")
        df = df.append(generate_df(pics, c))
    for c in touchesspe:
        pics, info = get_pics_from_file("../input/Hackaton/data/pics_" + c + ".bin")
        df = df.append(generate_df(pics, c))

    X = df[df.columns[:-1]]
    y = df['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(X_train, y_train)
    print("Accuracy on training set is : {}".format(clf.score(X_train, y_train)))
    print("Accuracy on test set is : {}".format(clf.score(X_test, y_test))) #56            99.5

    pics_loginmdp, info = get_pics_from_file("../input/Hackaton/data/pics_LOGINMDP.bin")
    
    #print(y_test.iloc[0])
    y_pred = pd.DataFrame(clf.predict(pics_loginmdp))
    y_pred.to_csv("result.csv")