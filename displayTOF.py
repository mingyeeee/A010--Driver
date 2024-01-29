import serial
import numpy as np
ser = serial.Serial("COM6", 1500000)
while True:
    data = str(ser.readline())
    if(data[2] == 'S'):
        print("S found")
        frame = data[data.find('S')+1:(data.find('N'))-1]
        #print(data.find('S'))
        #print((data.find('N')))
        ##print(frame)
        frame_array = np.array(frame.split(","))
        print(frame_array)
        if(frame_array.size == 10000):
            print("size ok")
        
    

