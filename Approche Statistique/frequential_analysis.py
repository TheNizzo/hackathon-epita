"""
Script python pour ouvrir les fichiers de traces de clavier

"""
import csv
import matplotlib.pyplot as plt
import numpy as np
import time

def read_int(f):
    ba = bytearray(4)
    f.readinto(ba)
    prm = np.frombuffer(ba, dtype=np.int32)
    return prm[0]
    
def read_double(f):
    ba = bytearray(8)
    f.readinto(ba)
    prm = np.frombuffer(ba, dtype=np.double)
    return prm[0]

def read_double_tab(f, n):
    ba = bytearray(8*n)
    nr = f.readinto(ba)
    if nr != len(ba):
        return []
    else:
        prm = np.frombuffer(ba, dtype=np.double)
        return prm
    
def get_pics_from_file(filename):
    # Lecture du fichier d'infos + pics detectes (post-processing KeyFinder)
    print("Ouverture du fichier de pics "+filename)
    f_pic = open(filename, "rb")
    info = dict()
    info["nb_pics"] = read_int(f_pic)
    print("Nb pics par trame: " + str(info["nb_pics"]))
    info["freq_sampling_khz"] = read_double(f_pic)
    print("Frequence d'echantillonnage: " + str(info["freq_sampling_khz"]) + " kHz")
    info["freq_trame_hz"] = read_double(f_pic)
    print("Frequence trame: " + str(info["freq_trame_hz"]) + " Hz")
    info["freq_pic_khz"] = read_double(f_pic)
    print("Frequence pic: " + str(info["freq_pic_khz"]) + " kHz")
    info["norm_fact"] = read_double(f_pic)
    print("Facteur de normalisation: " + str(info["norm_fact"]))
    tab_pics = []
    pics = read_double_tab(f_pic, info["nb_pics"])
    nb_trames = 1
    while len(pics) > 0:
        nb_trames = nb_trames+1
        tab_pics.append(pics)
        pics = read_double_tab(f_pic, info["nb_pics"])
    print("Nb trames: " + str(nb_trames))
    f_pic.close()
    return tab_pics, info

if __name__ == "__main__":
    tripletmoy = []
    tripletmed = []
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
    pics_ref, info = get_pics_from_file("../data/pics_LOGINMDP.bin")
    for j in range(0, len(alphabet)):
        pics_nokey, info = get_pics_from_file("../data/pics_" + alphabet[j] + ".bin")

        moyenne = np.mean(pics_nokey, axis=0)
        medianne = np.median(pics_nokey, axis=0)
        listemoy = []
        listemed = []
        for i in range(0, len(pics_ref)):
            distmoy = np.linalg.norm(pics_ref[i] - moyenne)
            distmed = np.linalg.norm(pics_ref[i] - medianne)
            listemoy.append(distmoy)
            listemed.append(distmed)
    
        for i in range(0, len(listemoy)):
            if listemoy[i] < 0.5:
                trimoy = (alphabet[j], i, listemoy[i])
                tripletmoy.append(trimoy)
            if listemed[i] < 0.5:
                trimed = (alphabet[j], i, listemed[i])
                tripletmed.append(trimed)

    touchesspe = ["CTRL", "ENTER", "NOKEY", "SHIFT", "SPACE", "SUPPR"]
    for j in range(0, len(touchesspe)):
        pics_nokey, info = get_pics_from_file("../data/pics_" + touchesspe[j] + ".bin")

        moyenne = np.mean(pics_nokey, axis=0)
        medianne = np.median(pics_nokey, axis=0)
        listemoy = []
        listemed = []
        for i in range(0, len(pics_ref)):
            distmoy = np.linalg.norm(pics_ref[i] - moyenne)
            distmed = np.linalg.norm(pics_ref[i] - medianne)
            listemoy.append(distmoy)
            listemed.append(distmed)
    
        for i in range(0, len(listemoy)):
            if listemoy[i] < 0.5:
                trimoy = (touchesspe[j], i, listemoy[i])
                tripletmoy.append(trimoy)
            if listemed[i] < 0.5:
                trimed = (touchesspe[j], i, listemed[i])
                tripletmed.append(trimed)



with open('moys.csv','w', newline='') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['name','num', 'coef'])
    for row in tripletmoy:
        csv_out.writerow(row)

with open('meds.csv','w', newline='') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['name','num', 'coef'])
    for row in tripletmoy:
        csv_out.writerow(row)
    exit()
