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

## PressKeyboard
import pyautogui
loop_on = False
sleep_after_press_delay = 1

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
fig_dims = (2,2) # figure size
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


######
## Press Keyboard funtion
######

#loop_stat
  # // 0 = no report
  # // 1 = this_loop_min decrease lower than min_thershold
  # // 2 = this_loop_max increase greater than max_thershold
  # // 3 = this_dif_negative_min decrease lower than negative_dif_thershold
  # // 4 = this_dif_postive_max increase greater than positive_dif_thershold

  # // 5 = same as 1, but extrem than factor extreme_lower_thershold
  # // 6 = same as 2, but extrem than factor extreme_upper_thershold
  # // 7 = same as 3, but extrem than factor extreme_upper_thershold
  # // 8 = same as 4, but extrem than factor extreme_upper_thershold
  
  # // 9 = abs_deviation > abs_deviation_thershold // temperature change much by pexel 
  # // 10 = abs_deviation > abs_deviation_thershold and > abs(deviation)*moving_deviation_factor // temperature change much by pexel, but all inside camera doesn't change so much // moving

def sleep_time(sleepy):
    print("waiting: ", sleepy)
    time.sleep(sleepy)

def sleep_after_press():
    # print("wait_standard: ", 5)
    #time.sleep(1.5)
    time.sleep(sleep_after_press_delay)

def load_track(deck):
    print("load_track: ", deck)
    if deck == 1:
        pyautogui.hotkey('shift', 'left')
    elif deck == 2:
        pyautogui.hotkey('shift', 'right')
    else:
        pyautogui.hotkey('shift', 'left')
        time.sleep(sleep_after_press_delay)
        pyautogui.hotkey('shift', 'right')
    sleep_after_press_delay

def play(deck):
    print("play: ", deck)
    if deck == 1:
        pyautogui.press('D')
    elif deck == 2:
        pyautogui.press('L')
    else:
        pyautogui.press('D')
        time.sleep(sleep_after_press_delay)
        pyautogui.press('L')
    sleep_after_press_delay

def tab_tempo(deck):
    print("tab_tempo: ", deck)
    if deck == 1:
        pyautogui.hotkey('shift', '!')
    elif deck == 2:
        pyautogui.hotkey('shift', '^')
    else:
        pyautogui.hotkey('shift', '!')
        time.sleep(sleep_after_press_delay)
        pyautogui.hotkey('shift', '^')
    sleep_after_press_delay

def sync_tempo(deck):
    print("sync_tempo: ", deck)
    if deck == 1:
        pyautogui.press('1')
    elif deck == 2:
        pyautogui.press('6')
    else:
        pyautogui.press('1')
        time.sleep(sleep_after_press_delay)
        pyautogui.press('6')
    sleep_after_press_delay
    
def auto_toggle():
    print("auto_toggle")
    pyautogui.hotkey('shift', 'f12')
    sleep_after_press_delay
    
def auto_next():
    print("auto_next")
    pyautogui.hotkey('shift', 'f11')
    sleep_after_press_delay

def loop_activate(deck, loop_status):
    if(loop_status):
        print("loop_OFF: ", deck)
        loop_status = False
    else:
        print("loop_ON: ", deck)
        pyautogui.press('q') # Set Loop In Point D1
        time.sleep(sleep_after_press_delay)
        pyautogui.press('u') # Set Loop In Point D2
        loop_status = True
        
    if deck == 1:
        pyautogui.press('q')
    elif deck == 2:
        pyautogui.press('u')
    else:
        pyautogui.press('q')
        time.sleep(sleep_after_press_delay)
        pyautogui.press('u')
    sleep_after_press_delay
    return loop_status
    
def loop_onoff(deck, loop_status):
    if(loop_status):
        print("loop_OFF: ", deck)
        loop_status = False
    else:
        print("loop_ON: ", deck)
        pyautogui.press('4') # Set Loop In Point D1
        time.sleep(sleep_after_press_delay)
        pyautogui.press('9') # Set Loop In Point D2
        loop_status = True
        
    if deck == 1:
        pyautogui.press('4')
    elif deck == 2:
        pyautogui.press('9')
    else:
        pyautogui.press('4')
        time.sleep(sleep_after_press_delay)
        pyautogui.press('9')
    sleep_after_press_delay
    return loop_status

def loop_in(deck):
    print("loop_out: ", deck)
    if deck == 1:
        pyautogui.press('2')
    elif deck == 2:
        pyautogui.press('7')
    else:
        pyautogui.press('2')
        time.sleep(sleep_after_press_delay)
        pyautogui.press('7')
    sleep_after_press_delay
    
def loop_out(deck):
    print("loop_out: ", deck)
    if deck == 1:
        pyautogui.press('3')
    elif deck == 2:
        pyautogui.press('8')
    else:
        pyautogui.press('3')
        time.sleep(sleep_after_press_delay)
        pyautogui.press('8')
    sleep_after_press_delay
    
def loop_halve(deck):
    print("loop_halve: ", deck)
    if deck == 1:
        pyautogui.press('w')
    elif deck == 2:
        pyautogui.press('i')
    else:
        pyautogui.press('w')
        time.sleep(sleep_after_press_delay)
        pyautogui.press('i')
    sleep_after_press_delay

def loop_double(deck):
    print("loop_double: ", deck)
    if deck == 1:
        pyautogui.press('e')
    elif deck == 2:
        pyautogui.press('o')
    else:
        pyautogui.press('e')
        time.sleep(sleep_after_press_delay)
        pyautogui.press('o')
    sleep_after_press_delay
    
def scratch(deck, delay, loop_on):
    print("scratch: ", deck, " delay", delay)
    loop_on = loop_activate(deck, loop_on)

    loop_halve(deck) 
    sleep_time(delay*2)
    loop_halve(deck)
    loop_halve(deck)
    sleep_time(delay*0.5)
    loop_double(deck)
    sleep_time(delay*0.7)
    loop_double(deck)
    sleep_time(delay)
    loop_double(deck)
    
    loop_on = loop_onoff(deck, loop_on)

    sleep_after_press_delay
    return loop_on
    
    
    



########
## read serial
########
loop_status = 0;
play_started = False;
play_last = 0;

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
            
            
            loop_status = int(float(serial_list[64]))
                      
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
            
            # print(serial_list[64:73])
            # print(serial_list[65])
            # print(serial_list[66])
            print(loop_status)
 
            t_array.append(time.monotonic()-t1)
            # print('SampleRate: {0:2.1f}fps'.format(len(t_array)/np.sum(t_array)))
            ser.flushInput()
            
            ### Consider PressKeyboard
            if(loop_status > 0 and play_last != loop_status):
                if(play_started):
                    if(loop_status < 9):
                        if(loop_status < 5):
                            sync_tempo(3)
                        else:
                            tab_tempo(3)
                    
                    elif(loop_status == 9):
                        loop_on = scratch(3,3,loop_on)
                    
                    elif(loop_status == 10):
                        auto_next()
                        
                else:
                    if(loop_status > 4):
                        auto_toggle()
                        play_started = True
                        play_last = loop_status
                                
                play_last = loop_status
                
            #print(play_last)

        except Exception as e:
            #print(e)
            #print(line)
            ser.flushInput()
            



