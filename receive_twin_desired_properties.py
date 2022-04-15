# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
import serial

ser = serial.Serial('COM4', 9600)


async def main():
    global ser
    # The connection string for a device should never be stored in code. For the sake of simplicity we're using an environment variable here.
    conn_str = "HostName=nha-kinh-iot-hub.azure-devices.net;DeviceId=demorasberry;SharedAccessKey=X0c5Bggoi4jZ8E+TxIeF2uPghFZeDLEaDPfg6th4fzA="
    # The client object is used to interact with your Azure IoT hub.
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # connect the client.
    print("Connecting to client")
    await device_client.connect()
    print("Connected")

    
    def uart_handler(receive_msg):
        print("The data receive from uart was: {}".format(receive_msg))
    
    
    twin = await device_client.get_twin()
    print('Got twin: ', twin)

    # define behavior for receiving a twin patch
    # NOTE: this could be a function or a coroutine
    def twin_patch_handler(patch):
        print("the data in the desired properties patch was: {}".format(patch))

    # set the twin patch handler on the client
    device_client.on_twin_desired_properties_patch_received = twin_patch_handler
    
    # define behavior for halting the application
    def stdin_listener():
        while True:
            if ser.in_waiting:
                receive_string = ser.readline().decode('unicode_escape').rstrip()
                uart_handler(receive_string)


    # Run the stdin listener in the event loop
    loop = asyncio.get_running_loop()
    user_finished = loop.run_in_executor(None, stdin_listener)

    # Wait for user to indicate they are done listening for messages
    await user_finished

    # Finally, shut down the client
    await device_client.shutdown()


if __name__ == "__main__":
    asyncio.run(main())

    # If using Python 3.6 use the following code instead of asyncio.run(main()):
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()