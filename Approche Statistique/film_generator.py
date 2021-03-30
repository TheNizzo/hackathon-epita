import csv
import matplotlib.pyplot as plt
import numpy as np
import time
import matplotlib.animation as animation

#set to 0 to have film with moys instead of meds
flag = 0

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


if flag == 0:
    tripletmed = tripletmoy


#reconstruct timeline
tripletmedsorted = sorted(tripletmed, key=lambda tup: tup[1])


listofmeds = []
for i in range(0, tripletmedsorted[-1][1] + 1):
    data = (["??"], i, [1])
    for j in range(0, len(tripletmedsorted)):
        
        k = j
        listoftouches = []
        listofcoeffs = []
            # if more than one detected keypress

        while (tripletmedsorted[k][1] == i):
            listoftouches.append(tripletmedsorted[k][0])
            listofcoeffs.append(tripletmedsorted[k][2])
            data = (listoftouches, i, listofcoeffs)
            k = k + 1
            if k >= len(tripletmed):
                print("NOPE")
                break
  
    
    listofmeds.append(data)

#plt.figure(1)
#plt.subplot(211)
#plt.scatter([x[1] for x in listofmeds], [x[0] for x in listofmeds], c=[2*x[2] for x in listofmeds], s=2)

# Fixing absciss
x = list(set([x[0] for x in tripletmedsorted]))
x.remove("NOKEY")
# histogram our data with numpy
data = [x[2] for x in listofmeds]

def barlist(n):
    ans = np.zeros(len(x))
    for key in x:
        if key in listofmeds[n][0]:
            indexpresent = x.index(key)
            position = listofmeds[n][0].index(key)
            valueofkey = data[n][position]
            ans[indexpresent] = 1 - valueofkey
         #   print(ans)

    return ans

fig=plt.figure(figsize=[19.2, 10.8])
plt.ylabel('confindence')
plt.xlabel('keys')
plt.grid(True)
plt.ylim((0,1))

n=len(listofmeds) #Number of frames
barcollection = plt.bar(x,barlist(0), 1, 0)

def animate(i):
    y=barlist(i+1)
    for i, b in enumerate(barcollection):
        b.set_height(y[i])

anim=animation.FuncAnimation(fig,animate,repeat=False,blit=False,frames=n-1,
                             interval=3)

plt.get_current_fig_manager().full_screen_toggle()
#anim.save('mymovie.mp4',writer=animation.FFMpegWriter(fps=10))
# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=333, metadata=dict(artist='Antonin Durand Seidl'))

anim.save('im.mp4', writer=writer)
