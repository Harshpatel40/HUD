import serial
import time
lidar_distance=100.0

def run_lidar():
    ser = serial.Serial('/dev/ttyUSB0',115200,timeout = 1)
    ser.write(bytes(b'B'))
    ser.write(bytes(b'W'))
    ser.write(bytes(2))
    ser.write(bytes(0))
    ser.write(bytes(0))
    ser.write(bytes(0))
    ser.write(bytes(1))
    ser.write(bytes(6))

    global lidar_distance
    while(True):
        while(ser.in_waiting >= 9):
            if((b'Y' == ser.read()) and ( b'Y' == ser.read())):
                Dist_L = ser.read()
                Dist_H = ser.read()
                Dist_Total = (ord(Dist_H) * 256) + (ord(Dist_L))
                for i in range (0,5):
                    ser.read()
            lidar_distance=Dist_Total/30.48
            #print(Dist_Total)