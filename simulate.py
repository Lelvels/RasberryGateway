import os
import random
import time
from azure.iot.device import IoTHubDeviceClient, Message
import json

# The device connection authenticates your device to your IoT hub. The connection string for 
# a device should never be stored in code. For the sake of simplicity we're using an environment 
# variable here. If you created the environment variable with the IDE running, stop and restart 
# the IDE to pick up the environment variable.
#
# You can use the Azure CLI to find the connection string:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table

CONNECTION_STRING = "HostName=nha-kinh-iot-hub.azure-devices.net;DeviceId=demorasberry;SharedAccessKey=X0c5Bggoi4jZ8E+TxIeF2uPghFZeDLEaDPfg6th4fzA="

def run_telemetry_sample(client):
    # This sample will send temperature telemetry every second
    print("IoT Hub device sending periodic messages")

    client.connect()
    mess_id = 1
    while True:
        # Build the message with simulated telemetry values.
        ArduinoId = "AR01"
        Temperature = random.randrange(10,30);
        Humidity = random.randrange(50, 80);
        SoilMoisture = random.randrange(10, 100);
        CO2 = random.randrange(3000, 10000);

        data = {
            "Id": mess_id,
            "ArduinoId" : ArduinoId,
            "Temperature": Temperature,
            "Humidity": Humidity,
            "SoilMoisture": SoilMoisture,
            "CO2": CO2
        }
        
        data_msg = json.dumps(data)
        message = Message(data_msg)

        # Send the message.
        print("Sending message: {}".format(message))
        client.send_message(message)
        print("Message successfully sent")
        time.sleep(5)


def main():
    print("IoT Hub Quickstart #1 - Simulated device")
    print("Press Ctrl-C to exit")

    # Instantiate the client. Use the same instance of the client for the duration of
    # your application
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    # Run Sample
    try:
        run_telemetry_sample(client)
    except KeyboardInterrupt:
        print("IoTHubClient sample stopped by user")
    finally:
        # Upon application exit, shut down the client
        print("Shutting down IoTHubClient")
        client.shutdown()

if __name__ == '__main__':
    main()