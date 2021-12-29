from serial import Serial
import time
ser = Serial('com6', 9600)
ser.timeout = 1

while(1):
    val = input('Enter value').strip() #strip gets rids of unneeded spaces
    ser.write(val.encode())