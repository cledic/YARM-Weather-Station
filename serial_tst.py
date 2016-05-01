#!/usr/bin/python

# -*- coding: utf-8 -*-
import string
import os
import re
import serial

_filepath="/tmp/images/"

#Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=15, xonxoff=False, rtscts=False, dsrdtr=False) 
ser.flushInput()
ser.flushOutput()

# aspetta 2 sec o CR
while True:
    sensor_data = ser.readline()
    print(sensor_data)
    output = open(_filepath+"sensor_1.txt","wb+")
    output.write( sensor_data)
    output.flush()
    os.fsync(output.fileno())
    output.close()

  
# variante
#While True:
    #bytesToRead = ser.inWaiting()
    #ser.read(bytesToRead)

