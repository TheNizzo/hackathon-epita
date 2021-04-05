"""
Script python pour ouvrir les fichiers de traces de clavier

"""

from pdb import set_trace
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import time
import itertools
from scipy.signal import find_peaks
import seaborn as sns
from scipy.fft import fft

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
    pics, info = get_pics_from_file("../input/Hackaton/data/pics_U.bin")
    pics_2, info = get_pics_from_file("../input/Hackaton/data/pics_H.bin")
    ######### Pics ############
    # NO KEY
    plt.figure(1)
    plt.subplot(111)
    pics = pics[:100]
    pics_2 = pics_2[:100]
    for i in range(len(pics)):
        plt.plot(range(1,info["nb_pics"]+1), pics[i])
        peaks, _ = find_peaks(pics[i])
    plt.xlabel('numéro de pic')
    plt.ylabel('valeur du pic')
    plt.title('no key')
    plt.grid(b=True, which='both')
    plt.figure(2)
    for i in range(len(pics_2)):
        plt.plot(range(1,info["nb_pics"]+1), pics_2[i])
        peaks, _ = find_peaks(pics_2[i])
    plt.grid(b=True, which='both')
    plt.show()
    
