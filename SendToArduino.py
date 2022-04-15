from pickle import GLOBAL
import serial # Module needed for serial communication
import time # Module needed to add delays in the code
import json
import random

ser = serial.Serial('COM4', 9600, timeout=1)
 
# Get rid of garbage/incomplete data
ser.flush()

def main():
    # Infinite loop
    while 1:
        ser.flush()
        humid = random.randint(40, 90)
        temp = random.randint(10, 30)
        desired = {'Id': 'AR01', 'Humidity': humid, 'Temperature': temp}
        send_string = json.dumps(desired)
        # Send the string. Make sure you encode it before you send it to the Arduino.
        ser.write(send_string.encode('utf-8'))
        print("Sending data: {0}".format(send_string))
        # Do nothing for 500 milliseconds (0.5 seconds)
        time.sleep(3)
        # Receive data from the Arduino
        while ser.in_waiting:
            receive_string = ser.readline().decode('unicode_escape').rstrip()
            #Print the data received from Arduino to the terminal
            print(receive_string)

if __name__ == '__main__':
    main()