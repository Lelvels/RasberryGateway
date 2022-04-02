from email import message
from http import client
import serial
from azure.iot.device import IoTHubDeviceClient, Message
import time

CONNECTION_STRING = "HostName=IoT-learning1.azure-devices.net;DeviceId=IotGateway;SharedAccessKey=rRiES1FldHlQ4xhNIMMr5Kx9XJkD2sOnd0pg3FYnQsY="
ser = serial.Serial('COM4', 9600, timeout = 1)
ser.reset_input_buffer()

def iothub_client_init():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

async def iothub_client_telementry_sample_run():
    client = iothub_client_init()
    print ( "IoT Hub device sending periodic messages")
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('unicode_escape').rstrip()
            msg_txt_format = line
            message = Message(msg_txt_format)
            print("Sending message: ")
            print(message)
            await client.send_message(message)
            print("Message sent")
            time.sleep(3)

if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telementry_sample_run()