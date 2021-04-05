import matplotlib.pyplot as plt
from read_pics import get_pics_from_file
import numpy as np
import pywt

""" Wavelet transform sur la touche H """

if __name__ == "__main__": 
    pics_pad0, info = get_pics_from_file("../input/Hackaton/data/pics_H.bin")
    list = [i for i in range(9)]
    list2 = [i for i in range(9, 18)]
    plot = [list, list2]
    
    figure, axis = plt.subplots(7, 7)
    for i in range(20):        
        axis[i // 7 , i % 7].plot(range(1,info["nb_pics"]+1), np.fft.fft(pics_pad0[i]), 'ko')
        plt.xlabel('numéro de pic')
        plt.ylabel('valeur du pic')
        plt.title('key A')
        plt.ylim(0, 1.5)
        plt.grid(b=True, which='both')
    for i in range(20):
        axis[(i + 28) // 7 , (i + 28) % 7].plot(plot, pywt.dwt(pics_pad0[i], 'db1'), 'ko')
        plt.xlabel('numéro de pic')
        plt.ylabel('valeur du pic')
        plt.title('key A')
        plt.ylim(0, 1.5)
        plt.grid(b=True, which='both')
    plt.show()
