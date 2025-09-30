#!/usr/bin/env python3
import random
## import RPi.GPIO as GPIO
from time import sleep
import serial
import statistics
## from influxdb import InfluxDBClient
from typing import NamedTuple

### Plot
import time,board
import numpy as np
import matplotlib.pyplot as plt



ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.reset_input_buffer()
min_read = 999.0
max_read = 0.0
loop_count = 0

readings = [0, 0]
max_samples = 10


## Plot
mlx_shape = (8,8)

# setup the figure for plotting
plt.ion() # enables interactive plotting
fig,ax = plt.subplots(figsize=(12,7))
therm1 = ax.imshow(np.zeros(mlx_shape),vmin=0,vmax=60) #start plot with zeros
cbar = fig.colorbar(therm1) # setup colorbar for temps
cbar.set_label('Temperature [$^{\circ}$C]',fontsize=14) # colorbar label

frame = np.zeros((8*8,)) # setup array for storing all 64 temperatures
t_array = []
print("Starting loop")

########
## read serial
########
while True:
    t1 = time.monotonic()
    if ser.in_waiting > 0:
        # try:          
            line = ser.readline().decode('utf-8').rstrip()
            # print(line)
            serial_list = line.split(",")
            #serial_val = list(map(float, line.split(",")))
            serial_val = [float(idx) for idx in serial_list[:64]]
            #print(serial_val)
            #serial_float = serial_val.astype(float)
            frame = np.array(serial_val[:64])
            #print(frame)
            
                      

                
            ## mlx.getFrame(frame) # read MLX temperatures into frame var
            data_array = (np.reshape(frame,mlx_shape)) # reshape to 24x32
            therm1.set_data(np.fliplr(data_array)) # flip left to right
            #therm1.set_clim(vmin=np.min(data_array),vmax=np.max(data_array)) # set bounds
            therm1.set_clim(vmin=10,vmax=25) # set bounds
            cbar.update_normal(therm1) # update colorbar range
            plt.title(f"Max Temp: {np.max(data_array):.1f}C")
            plt.pause(0.001) # required
            #fig.savefig('mlx90640_test_fliplr.png',dpi=300,facecolor='#FCFCFC', bbox_inches='tight') # comment out to speed up
            t_array.append(time.monotonic()-t1)
            print('Sample Rate: {0:2.1f}fps'.format(len(t_array)/np.sum(t_array)))


def mean(nums):
    return float(sum(nums)) / max(len(nums), 1)
