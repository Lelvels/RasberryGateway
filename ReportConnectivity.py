from http import client
from pydoc import cli
import time
from azure.iot.device import IoTHubModuleClient
from janus import T
import serial
import json

#CONNECTION STRING CỦA THIẾT BỊ => CODE CHẠY TRÊN RAS BERRY
CONNECTION_STRING = "HostName=nha-kinh-iot-hub.azure-devices.net;DeviceId=demorasberry;SharedAccessKey=X0c5Bggoi4jZ8E+TxIeF2uPghFZeDLEaDPfg6th4fzA="
ser = serial.Serial('COM4', 9600)

def get_sensor_data():
    print("Reading from serial!")
    data = ser.readline().decode('unicode_escape').rstrip()
    data = json.loads(data)
    arduino_id = data["ArduinoId"] 
    humid = data["Humidity"]
    temp = data["Temperature"]
    light = data["LuminousIntensity"]
    dict ={ 
        'SensorParameters' : {
            arduino_id : {
                'Humidity' : humid,
                'Temperature' : temp,
                'LuminousIntensity' : light    
            }
        }
    }
    return dict

def get_desired_data(client, arduino_id):
    twin_patch = client.receive_twin_desired_properties_patch()
    myData = twin_patch['DesiredParameters'][arduino_id]
    desired_data = {arduino_id : myData}
    return desired_data

#Hàm để tạo client
def create_client():
    try:
        client = IoTHubModuleClient.create_from_connection_string(CONNECTION_STRING)
    except:
        client.shutdown()
    return client

def main():
    print("Starting the py Iot Hub Device Twin device sample...")
    client = create_client()
    print("IoTHubModuleClient waiting for commands")
    
    try:    
        desired_data = get_desired_data(client=client, arduino_id="AR01")
        print(desired_data)
        print("Sending data as reported property...")
        
        # while ser.readline():
        #     reported_patch = get_sensor_data()
        #     print(reported_patch)
        #     client.patch_twin_reported_properties(reported_patch)
        #     print("Reported properties updated")
            
    except KeyboardInterrupt:
        print("Iot Hub Device Twin device sample stopped")
    finally:
        print("Shutting down IoT Hub client")
        ser.close()
        client.shutdown()

if __name__ == '__main__':
    main()    
    