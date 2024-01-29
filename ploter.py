IMAGE_SIZE = 100
import numpy as np
import matplotlib.pyplot as plt

import serial
import numpy as np
ser = serial.Serial("COM6", 1500000)

plt.ion()

fig1, ax1 = plt.subplots()
#fig2, ax2 = plt.subplots()
#fig3, ax3 = plt.subplots()

# In order to solve this, one needs to set the color scale with vmin/vman
# I found this, thanks to @jettero's comment.
array = np.zeros(shape=(IMAGE_SIZE, IMAGE_SIZE), dtype=np.float64)
#axim2 = ax2.imshow(array, vmin=0, vmax=99)

# alternatively this process can be automated from the data
array[0, 0] = 2500 # this value allow imshow to initialise it's color scale
axim1 = ax1.imshow(array)

del array

while True:
    data = str(ser.readline())
    if(data[2] == 'S'):
        print("S found")
        frame = data[data.find('S')+1:(data.find('N'))-1]
        #print(data.find('S'))
        #print((data.find('N')))
        ##print(frame)

        #print(frame)
        frame_2 = frame.split(",")
        print(len(frame_2))
        if(len(frame_2) == 10000):
            print("size ok")
            frame_array = np.array([pow(float(int(x, 16))/5.1,2) for x in frame_2])
        
            print(type(frame_array))
            frame_matrix = frame_array.reshape(100,100)

            axim1.set_data(frame_matrix)
            fig1.canvas.flush_events()
            
            #axim2.set_data(matrix)
            #fig1.canvas.flush_events()
