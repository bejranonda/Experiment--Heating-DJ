import serial
import time

# interp function
def write_serial(txt):
    print(txt) 
    txt = txt + "\n"
    write_ser.write(txt.encode())     # write a string
    time.sleep(4);
    
#write_ser = serial.Serial('/dev/ttyUSB1')  # open serial port
write_ser = serial.Serial('/dev/ttyUSB1', 57600, timeout=5)
print(write_ser.name)         # check which port was really used
print("Waiting")         # check which port was really used
time.sleep(5);
write_serial("test   ")         # check which port was really used
write_serial("slow        ,9")         # check which port was really used
write_serial("fast        ,2")         # check which port was really used
write_serial("pac,p")     # write a string
write_serial("<    ,1")     # write a string
write_serial("COOL ,9")     # write a string
write_serial("Wowww Hot    ,2")     # write a string
write_serial("pac-fast       ,p2")     # write a string
write_ser.close()             # close port