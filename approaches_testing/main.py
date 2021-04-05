from math import gamma
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
import seaborn as sns
from data_clean import detect_outliers
from scipy.fft import fft
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB

if __name__ == "__main__":
    alphanum = "abcdefghijklmnopqrstuvwxyz0123456789"
    touchesspe = ["CTRL", "ENTER", "NOKEY", "SHIFT", "SPACE", "SUPPR"]
    n = 0
    i = 0
    df = pd.DataFrame()
    df_1 = pd.DataFrame()
    for c in alphanum:
        pics, info = get_pics_from_file("../input/Hackaton/data/pics_" + c + ".bin")
        n += len(pics)
        ff = []
        df_test = generate_df(pics, c)
        df_temp = detect_outliers(df_test)
        df_temp['label'] = c
        df = df.append(df_temp)
        df_1 = df_1.append(df_test)
        
        i += 1
    for c in touchesspe:
        pics, info = get_pics_from_file("../input/Hackaton/data/pics_" + c + ".bin")
        n += len(pics)
        df_test = generate_df(pics, c)
        df_temp = detect_outliers(df_test)
        df_temp['label'] = c
        df = df.append(df_temp)
        df_1 = df_1.append(df_test)
        
        i += 1
    n /= i
    X = df[df.columns[:-1]]
    y = df['label']
    X1 = df_test[df_test.columns[:-1]]
    y1 = df_test['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
    X_train1, X_test1, y_train1, y_test1 = train_test_split(X1, y1, test_size=0.1)
    
 
    #RandomForestClassifier
    clf = RandomForestClassifier()
    rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid, n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1)
    clf.fit(X_train, y_train)
    print("Accuracy on training set is : {}".format(clf.score(X_train, y_train)))
    print("Accuracy on test set is : {}".format(clf.score(X_test1, y_test1))) #56            99.5



    #SGD Classifier
    clf = make_pipeline(StandardScaler(),
    SGDClassifier(max_iter=100000, tol=1e-3))
    clf.fit(X_train, y_train)
    print("Accuracy on training set is : {}".format(clf.score(X_train, y_train)))
    print("Accuracy on test set is : {}".format(clf.score(X_test1, y_test1)))

    pics_loginmdp, info = get_pics_from_file("../input/Hackaton/data/pics_LOGINMDP.bin")
    

    #Kneighbours
    neigh = KNeighborsClassifier(n_neighbors=int(n))
    neigh.fit(X_train, y_train)
    print("Accuracy on training set is : {}".format(neigh.score(X_train, y_train)))
    print("Accuracy on test set is : {}".format(neigh.score(X_test1, y_test1)))
    
    #SVC
    clf = make_pipeline(StandardScaler(), SVC(gamma='auto'))
    clf.fit(X_train, y_train)
    clf = make_pipeline(StandardScaler(),
    LinearSVC(random_state=0, tol=1e-4, max_iter=1000, dual=False))
    clf.fit(X_train, y_train)
    print("Accuracy on training set is : {}".format(clf.score(X_train, y_train)))
    print("Accuracy on test set is : {}".format(clf.score(X_test1, y_test1)))


    #GNB
    gnb = GaussianNB()
    gnb.fit(X_train, y_train)
    y_pred = pd.DataFrame(gnb.predict(pics_loginmdp))
    y_pred.to_csv("result_login_gnb.csv")

    print("Accuracy on training set is : {}".format(gnb.score(X_train, y_train)))
    print("Accuracy on test set is : {}".format(gnb.score(X_test1, y_test1)))

