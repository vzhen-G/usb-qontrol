import serial
import re
import time

# define the values format
value_format = '\d+\.\d+'
nup_format = ''
vfull_format = ''
error_format = ''

def Qontrol_Init():
    # open the serial port
    heater = serial.Serial("COM5", 115200, timeout=1) 
    if not(heater.is_open):
        raise ValueError('Device not found')
    heater.flush()
    d = heater.write(b'nupall?\n')
    time.sleep(1)
    nup_result = heater.read(1024)
    print(nup_result)
    print(heater.name)
    heater.close()










Qontrol_Init()
