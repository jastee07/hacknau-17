#import libraries
import serial
import time

#make serial connection to Arduino
ser = serial.Serial('/dev/cu.usbmodem1461', 9600)

#create / append to output file
output = open("arduino_temp.txt", 'w')

#infinite loop to get data
while True:
    #get temperature on delay
    time.sleep(.2)
    temp = float(ser.readline())

    #if temperature is not an expected value, break loop
    if temp < 0 or temp > 110:
        break

    #save temp to output file
    output.write("{}\n".format(temp))

#close file if loop broken
output.close()