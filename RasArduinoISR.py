from importlib.util import decode_source
import json
from pydoc import cli
from requests import patch
import serial # Module needed for serial communication
import asyncio
import json
from azure.iot.device import IoTHubModuleClient

def is_float(element) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False
    
def is_json(element) -> bool:
    try:
        json.loads(element)
    except ValueError as e:
        return False
    return True

def create_client(connection_string):
    try:
        client = IoTHubModuleClient.create_from_connection_string(connection_string)
    except:
        client.shutdown()
    return client

def get_sensor_data(reported_data):
    data = json.loads(reported_data)
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
    return dict

def get_desired_data(client):
    twin = client.get_twin()
    if 'desired' in twin:
        arduino_id = "AR01"
        temp = twin['desired']['DesiredParameters'][arduino_id]['Temperature']
        humid = twin['desired']['DesiredParameters'][arduino_id]['Humidity']
        desired = {'ArduinoId': arduino_id, 'Humidity': humid, 'Temperature': temp}
        send_string = json.dumps(desired)
        send_string = send_string
    return send_string.encode('unicode_escape')
        
def standard_desired_data(patch):
    arduino_id = "AR01"
    desired_data = patch['DesiredParameters'][arduino_id]
    temp = desired_data['Temperature']
    humid = desired_data['Humidity']
    desired = {'ArduinoId':arduino_id, 'Humidity':humid, 'Temperature':temp}
    result_string = json.dumps(desired)
    return result_string.encode('unicode_escape')

async def main():
    try:
        #Init code here
        ser = serial.Serial('COM4', 9600, timeout=1)
        print("Starting the py Iot Hub Device Twin device sample...")
        client = create_client("HostName=nha-kinh-iot-hub.azure-devices.net;DeviceId=demorasberry;SharedAccessKey=X0c5Bggoi4jZ8E+TxIeF2uPghFZeDLEaDPfg6th4fzA=")
        print("Connecting to client")
        client.connect()
        print("Connected")
        #End of Init code
        
        def uart_listener():
            #Thêm handler vào nhưng bị lỗi không cập nhật ???
            #desired_data = get_desired_data(client)
            # def desired_handler(patch):
            #     desired_data = standard_desired_data(patch=patch)
            #     print("Desired data update: ", desired_data)
            # client.on_twin_desired_properties_patch_received = desired_handler
            
            while True:
                #Wait for arduino to send reported data
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').rstrip()
                    print(line)
                    if is_json(line): 
                        report_data = get_sensor_data(line);
                        print(report_data)
                        client.patch_twin_reported_properties(report_data)
                        print("Reported properties updated")
                    elif line == "DHT_ERR":
                        print("DHT error!")
                    else:
                        print("Exception string!")
                    
                    #Send desired data
                    desired_data = get_desired_data(client)
                    ser.write(desired_data)
                    print(desired_data)
                    print("Desired data sent!")
            
        # Run the stdin listener in the event loop
        loop = asyncio.get_running_loop()
        user_finished = loop.run_in_executor(None, uart_listener)

        # Wait for user to indicate they are done listening for messages
        await user_finished
    except KeyboardInterrupt:
        print("Rasberry stopped")
    finally:
        ser.close()
        client.shutdown()
        print("Shutting down IoT Hub client")

if __name__ == '__main__':
    asyncio.run(main())
    