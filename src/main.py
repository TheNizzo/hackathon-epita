from read_pics import get_pics_from_file
from legacy import mean_from_pic, generate_df
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from test_classifiers import run_exps
from hypertuning import random_grid
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

if __name__ == "__main__":
    alphanum = "abcdefghijklmnopqrstuvwxyz0123456789"
    touchesspe = ["CTRL", "ENTER", "NOKEY", "SHIFT", "SPACE", "SUPPR"]
    n = 0
    i = 0
    df = pd.DataFrame()
    for c in alphanum:
        pics, info = get_pics_from_file("../input/Hackaton/data/pics_" + c + ".bin")
        n += len(pics)
        df = df.append(generate_df(pics[0:int(len(pics) / 20)], c))
        i += 1
    for c in touchesspe:
        pics, info = get_pics_from_file("../input/Hackaton/data/pics_" + c + ".bin")
        n += len(pics)
        df = df.append(generate_df(pics[0:int(len(pics) / 20)], c))
        i += 1
    n /= i
    X = df[df.columns[:-1]]
    y = df['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4
    )

    #RandomForestClassifier
    clf = RandomForestClassifier()
    #rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid, n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1)
    clf.fit(X_train, y_train)
    print("Accuracy on training set is : {}".format(clf.score(X_train, y_train)))
    print("Accuracy on test set is : {}".format(clf.score(X_test, y_test))) #56            99.5


    #print(run_exps(X_train, y_train, X_test, y_test))

    #SGD Classifier
    # clf = make_pipeline(StandardScaler(),
    #     SGDClassifier(max_iter=100000, tol=1e-3))
    # clf = 
    # clf.fit(X_train, y_train)
    # print("Accuracy on training set is : {}".format(clf.score(X_train, y_train)))
    # print("Accuracy on test set is : {}".format(clf.score(X_test, y_test)))

    #pics_loginmdp, info = get_pics_from_file("../input/Hackaton/data/pics_LOGINMDP.bin")
    
    #print(y_test.iloc[0])
    # y_pred = pd.DataFrame(clf.predict(pics_loginmdp))
    # y_pred.to_csv("result.csv")

    #Kneighbours
    # neigh = KNeighborsClassifier(n_neighbors=int(n))
    # neigh.fit(X_train, y_train)

    #SVC
    # clf = make_pipeline(StandardScaler(), SVC(gamma='auto'))
    # #import pdb; pdb.set_trace()
    # clf.fit(X_train, y_train)
    # print("Accuracy on training set is : {}".format(clf.score(X_train, y_train)))
    # print("Accuracy on test set is : {}".format(clf.score(X_test, y_test)))