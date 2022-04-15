import asyncio
import random
from azure.iot.device.aio import IoTHubDeviceClient


async def main():
    conn_str = "HostName=nha-kinh-iot-hub.azure-devices.net;DeviceId=demorasberry;SharedAccessKey=X0c5Bggoi4jZ8E+TxIeF2uPghFZeDLEaDPfg6th4fzA="
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # connect the client.
    await device_client.connect()

    # update the reported properties
    reported_properties = {"temperature": random.randint(320, 800) / 10}
    print("Setting reported temperature to {}".format(reported_properties["Temperature"]))
    await device_client.patch_twin_reported_properties(reported_properties)

    # Finally, shut down the client
    await device_client.shutdown()


if __name__ == "__main__":
    asyncio.run(main())

    # If using Python 3.6 use the following code instead of asyncio.run(main()):
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()