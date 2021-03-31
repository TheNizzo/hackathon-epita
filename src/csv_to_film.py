import csv
import matplotlib.pyplot as plt
import numpy as np
import time
import matplotlib.animation as animation


listofmeds = []
with open('result_login3.csv', newline='') as f:
    reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
    for row in reader:
        if len(row) == 1:
            listofmeds.append(("NOKEY", row[0], [0.1]))
        else:
            listofmeds.append((row[1], row[0], [0.1]))

n=len(listofmeds)  #Number of frames


# Fixing absciss
x = list(set([x[0] for x in listofmeds]))
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

anim.save('ia_answer.mp4', writer=writer)
