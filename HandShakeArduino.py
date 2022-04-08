from http import client
from pickle import GLOBAL
from tempfile import tempdir
from unittest.mock import patch
import serial # Module needed for serial communication
import time # Module needed to add delays in the code
import json
import random
import enum
from azure.iot.device import IoTHubModuleClient
import asyncio

CONNECTION_STRING = "HostName=nha-kinh-iot-hub.azure-devices.net;DeviceId=demorasberry;SharedAccessKey=X0c5Bggoi4jZ8E+TxIeF2uPghFZeDLEaDPfg6th4fzA="
ser = serial.Serial('COM4', 9600, timeout=1)
ser.flush()

class DataStateFlag(enum.Enum):
    IDLE = 0
    SendingReportedData = 1
    ReceiveDesiredData = 2

def create_client():
    try:
        client = IoTHubModuleClient.create_from_connection_string(CONNECTION_STRING)
    except:
        client.shutdown()
    return client

def get_sensor_data(reported):
    data = json.loads(reported)
    arduino_id = data["ArduinoId"] 
    humid = data["Humidity"]
    temp = data["Temperature"]
    dict ={ 
        'SensorParameters' : {
            arduino_id : {
                'Humidity' : humid,
                'Temperature' : temp
            }
        }
    }
    return dict;    

def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True

def get_desired_data(client, arduino_id):
    twin_patch = client.receive_twin_desired_properties_patch()
    myData = twin_patch['DesiredParameters'][arduino_id]
    desired_data = {arduino_id : myData}
    return desired_data

def init_reported_data(client):
    twin = client.get_twin()
    if 'desired' in twin:
        arduino_id = "AR01"
        temp = twin['desired']['DesiredParameters'][arduino_id]['Temperature']
        humid = twin['desired']['DesiredParameters'][arduino_id]['Humidity']
        desired = {'ArduinoId': arduino_id, 'Humidity': humid, 'Temperature': temp}
        send_string = json.dumps(desired)
    return send_string
        
def standard_desired_data(patch):
    arduino_id = "AR01"
    desired_data = patch['DesiredParameters'][arduino_id]
    temp = desired_data['Temperature']
    humid = desired_data['Humidity']
    desired = {'ArduinoId':arduino_id, 'Humidity':humid, 'Temperature':temp}
    result_string = json.dumps(desired).rstrip()
    return result_string

async def main():
    try:
        global ser
        print("Starting the py Iot Hub Device Twin device sample...")
        client = create_client()
        print("Connecting to client")
        client.connect()
        print("Connected")
                
        def uart_listener():
            #Setup reported data
            reported_data = ""
            
            #Setup desired data
            desired_data = init_reported_data(client)
            print(desired_data)
            
            #Add listener handler
            def desired_handler(patch):
                desired_data = standard_desired_data(patch)
                print("Desired data updated:", desired_data)

            client.on_twin_desired_properties_patch_received = desired_handler
            
            while True: 
                if ser.in_waiting:
                    receive_string = ser.readline().decode('unicode_escape').rstrip()
                    #Print the data received from Arduino to the terminal
                    if (receive_string == "AR01"):
                        print("Reported data receiver start!")
                        ser.write("ACK".encode('unicode_escape'))
                    elif (receive_string == "SENSOR_ERR"):
                        print("Arduino failed to read from sensor!")
                    elif (receive_string == "STOP"):
                        #Nhan du chuoi va bat dau gui len cloud
                        print(desired_data)
                        ser.write(desired_data.encode('unicode_escape'))
                        print("Reported data receiver stop!")
                        time.sleep(1)
                    else:
                        if(is_json(receive_string)):
                            reported_data = receive_string
                            reported_patch = get_sensor_data(reported_data)
                            print("Reported patch: {0}".format(reported_data))
                            #client.patch_twin_reported_properties(reported_patch)
                            print("Reported properties updated!")
                        else:
                            print(receive_string)
               
        # Run the stdin listener in the event loop
        loop = asyncio.get_running_loop()
        user_finished = loop.run_in_executor(None, uart_listener)

        # Wait for user to indicate they are done listening for messages
        await user_finished

        # Finally, shut down the client
        client.shutdown()
    except KeyboardInterrupt:
        print("Iot Hub Device Twin device sample stopped")
    finally:
        ser.close()
        client.shutdown()
        print("Shutting down IoT Hub client")
                
if __name__ == '__main__':
    asyncio.run(main())