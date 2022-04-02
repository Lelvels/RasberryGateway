from http import client
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

def get_desired_data():
    
    return 

#Hàm để tạo client
def create_client():
    client = IoTHubModuleClient.create_from_connection_string(CONNECTION_STRING)
    def twin_patch_handler(twin_patch):
        print("Twin patch received:")
        print(twin_patch)
    try:
        #Set handler on the client
        client.on_twin_desired_properties_patch_received = twin_patch_handler
    except:
        client.shutdown()
    
    return client

def main():
    print("Starting the py Iot Hub Device Twin device sample...")
    client = create_client()
    print("IoTHubModuleClient waiting for commands")
    
    try:
        print("Sending data as reported property...")
        while ser.readline():
            reported_patch = get_sensor_data()
            print(reported_patch)
            client.patch_twin_reported_properties(reported_patch)
            print("Reported properties updated")
    except KeyboardInterrupt:
        print("Iot Hub Device Twin device sample stopped")
    finally:
        print("Shutting down IoT Hub client")
        ser.close()
        client.shutdown()

if __name__ == '__main__':
    main()    
    