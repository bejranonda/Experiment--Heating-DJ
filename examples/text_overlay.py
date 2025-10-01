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
from scipy import interpolate
from skimage.transform import resize

write_ser = serial.Serial('/dev/ttyUSB1', 57600, timeout=5)

def write_serial(txt):
    print(txt) 
    txt = txt + "\n"
    write_ser.write(txt.encode())     # write a string

def mean(nums):
    return float(sum(nums)) / max(len(nums), 1)


# interp function
def interp(z_var):
    # cubic interpolation on the image
    # at a resolution of (pix_mult*8 x pix_mult*8)
    f = interpolate.interp2d(xx,yy,z_var,kind='cubic')
    return f(grid_x,grid_y)
         
#ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=None)
ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=None)
ser.reset_input_buffer()
min_read = 999.0
max_read = 0.0
loop_count = 0

readings = [0, 0]
max_samples = 10

# ## Interpolate
# ### scipy
# X = np.linspace(0,7,8)
# Y = np.linspace(0,7,8)
# x,y = np.meshgrid(X,Y)
# Xnew = np.linspace(0,8,32)
# Ynew = np.linspace(0,8,32)
# ### skimage
# dim1, dim2 = 16, 16


## Plot
# mlx_shape = (8,8)

# setup the figure for plotting
# plt.ion() # enables interactive plotting
# fig,ax = plt.subplots(figsize=(12,7))
# therm1 = ax.imshow(np.zeros(mlx_shape),vmin=0,vmax=60) #start plot with zeros
# cbar = fig.colorbar(therm1) # setup colorbar for temps
# cbar.set_label('Temperature [$^{\circ}$C]',fontsize=14) # colorbar label

frame = np.zeros((8*8,)) # setup array for storing all 64 temperatures
t_array = []
print("Starting loop")
line = []

#####################################
# Interpolation Properties 
#####################################
#
# original resolution
pix_res = (8,8) # pixel resolution
xx,yy = (np.linspace(0,pix_res[0],pix_res[0]),
                    np.linspace(0,pix_res[1],pix_res[1]))
zz = np.zeros(pix_res) # set array with zeros first
# new resolution
pix_mult = 5 # multiplier for interpolation 
interp_res = (int(pix_mult*pix_res[0]),int(pix_mult*pix_res[1]))
grid_x,grid_y = (np.linspace(0,pix_res[0],interp_res[0]), np.linspace(0,pix_res[1],interp_res[1]))
grid_z = interp(zz) # interpolated image

#
#####################################
# Start and Format Figure 
#####################################
#
plt.rcParams.update({'font.size':16})
fig_dims = (9,9) # figure size
fig,ax = plt.subplots(figsize=fig_dims) # start figure
#fig.canvas.set_window_title('AMG8833 Image Interpolation')
cmap_use = "jet" # color map
#cmap_use = plt.cm.RdBu_r # color map
#im1 = ax.imshow(grid_z,vmin=18,vmax=37,cmap=plt.cm.RdBu_r) # plot image, with temperature bounds
im1 = ax.imshow(grid_z,vmin=18,vmax=37,cmap=cmap_use) # plot image, with temperature bounds
cbar = fig.colorbar(im1,fraction=0.0475,pad=0.03) # colorbar
cbar.set_label('Temperature [C]',labelpad=10) # temp. label
fig.canvas.draw() # draw figure

ax_bgnd = fig.canvas.copy_from_bbox(ax.bbox) # background for speeding up runs
fig.show() # show figure

pix_to_read = 64 # read all 64 pixels




########
## read serial
########
while True:
    t1 = time.monotonic()
    if ser.in_waiting > 0:
        try:          
            line = ser.readline().decode('utf-8').rstrip()
            # print(line)
            serial_list = line.split(",")
            #print(serial_list)
            #serial_val = list(map(float, line.split(",")))
            serial_val = [float(idx) for idx in serial_list[:64]]
            #print(serial_val)
            #serial_float = serial_val.astype(float)
            frame = np.array(serial_val[:64])
            #print(frame)
            
                      
            ## Interpolate
            ### scipy
            # f = interpolate.interp2d(x,y,frame,kind='cubic')
            # grid_interplote = f(Xnew,Ynew)
            # print(grid_interplote)
            ### skimage
            #grid_interplote = resize(frame,(dim1,dim2))
            #print(grid_interplote)
            #data_array = grid_interplote
            
            # ## mlx.getFrame(frame) # read MLX temperatures into frame var
            # data_array = (np.reshape(frame,mlx_shape)) # reshape to 24x32
            # therm1.set_data(np.fliplr(data_array)) # flip left to right
            # #therm1.set_clim(vmin=np.min(data_array),vmax=np.max(data_array)) # set bounds
            # therm1.set_clim(vmin=10,vmax=25) # set bounds
            # cbar.update_normal(therm1) # update colorbar range
            # plt.title(f"Max Temp: {np.max(data_array):.1f}C")
            # plt.pause(0.001) # required
            # #fig.savefig('mlx90640_test_fliplr.png',dpi=300,facecolor='#FCFCFC', bbox_inches='tight') # comment out to speed up
            
            # data_array = grid_interplote
            # ## mlx.getFrame(frame) # read MLX temperatures into frame var
            # #data_array = (np.reshape(frame,mlx_shape)) # reshape to 24x32
            # therm1.set_data(np.fliplr(data_array)) # flip left to right
            # #therm1.set_data(data_array)
            # #therm1.set_clim(vmin=np.min(data_array),vmax=np.max(data_array)) # set bounds
            # therm1.set_clim(vmin=10,vmax=25) # set bounds
            # cbar.update_normal(therm1) # update colorbar range
            # plt.title(f"Max Temp: {np.max(data_array):.1f}C")
            # plt.pause(0.001) # required
            # #fig.savefig('mlx90640_test_fliplr.png',dpi=300,facecolor='#FCFCFC', bbox_inches='tight') # comment out to speed up
            # t_array.append(time.monotonic()-t1)
            
            fig.canvas.restore_region(ax_bgnd) # restore background (speeds up run)
            new_z = interp(np.reshape(frame,pix_res)) # interpolated image
            ## new_z = interp(np.fliplr(np.reshape(frame,pix_res))) # interpolated image
            im1.set_data(new_z) # update plot with new interpolated temps
            im1.set_clim(vmin=10,vmax=20) # set bounds
            ax.draw_artist(im1) # draw image again
            fig.canvas.blit(ax.bbox) # blitting - for speeding up run
            fig.canvas.flush_events() # for real-time plot
            plt.pause(0.001) # required
            
            #print(serial_list[64:73])
            # print(serial_list[65])
            # print(serial_list[66])
            if(float(serial_list[64]) > 0):
                #print(type(serial_list[64]))
                txt_int = 10 - int(float(serial_list[64]))
                write_serial(str(serial_list[64]) + "   ," + str(txt_int)) 
 
            t_array.append(time.monotonic()-t1)
            print('SampleRate: {0:2.1f}fps'.format(len(t_array)/np.sum(t_array)))
            ser.flushInput()
            
        except Exception as e:
            #print(e)
            #print(line)
            ser.flushInput()
            



