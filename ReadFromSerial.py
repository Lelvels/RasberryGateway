import serial 
import json
import time
from azure.iot.device import IoTHubDeviceClient, Message
         

CONNECTION_STRING = "HostName=IoT-learning1.azure-devices.net;DeviceId=demorasberry;SharedAccessKey=o7VG4ugwljuY9+fnfRlqD9TdRG2c7+g4n4IciXTEfxY="
MSG_TXT = '{{"message_id":{mess_id},"device_id":"{device_id}","temperature":{temperature},"humidity":{humidity}}}'
ser = serial.Serial('COM6',9600)


def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def iothub_client_telemetry_sample_run():
    mess_id = 0
    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )
        while (True):
            data = ser.readline().decode('unicode_escape').rstrip()
            
            class Payload(object):
                def __init__(self, data):
                    self.__dict__ = json.loads(data)

            p = Payload(data)
            h = p.Humidity
            t = p.Temperature
            de_id = p.deviceID
            mess_id += 1
            msg_txt_formatted = MSG_TXT.format(temperature=t, humidity=h, device_id = de_id,mess_id = mess_id)  
            #message = Message(msg_txt_formatted)
            
            message = Message(msg_txt_formatted)
            print(f"Sending message: {message}")
            client.send_message(message)
            print ( "Message successfully sent" )
            time.sleep(5)
            
    except KeyboardInterrupt:                                           
        print('Done')
    finally:
        ser.close()
        
if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()