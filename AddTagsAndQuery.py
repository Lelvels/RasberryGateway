from ast import In
from socketserver import DatagramRequestHandler
import sys
from time import sleep
from tkinter.tix import Select
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import Twin, TwinProperties, QuerySpecification, QueryResult

#IOT HUB CONNECTION STRING - HOSTNAME - SharedAccessKeyName - SharedAccessKey => CODE CHẠY TRÊN CLIENT
IOTHUB_CONNECTION_STRING = "HostName=nha-kinh-iot-hub.azure-devices.net;SharedAccessKeyName=registryWriteAndServiceConnect;SharedAccessKey=LBEhfGJJ7SxMmCK09qmGUm7cw5LezgK8nM5Pq7uXgSQ="
DEVICE_ID = "demorasberry"

def get_desired_data(id, humid, temp):
    print("Getting desired data!")
    arduino_id = id
    desired_humid = humid
    desired_temp = temp
    dict = {
        'DesiredParameters' : {
            arduino_id : {
                'Humidity' : desired_humid,
                'Temperature' : desired_temp
            }
        }
    }
    return dict

def print_twin(title, iothub_device):
    print(title + ":")
    print("device_id                      = {0}".format(iothub_device.device_id))
    print("module_id                      = {0}".format(iothub_device.module_id))
    print("authentication_type            = {0}".format(iothub_device.authentication_type))
    print("x509_thumbprint                = {0}".format(iothub_device.x509_thumbprint))
    print("etag                           = {0}".format(iothub_device.etag))
    print("device_etag                    = {0}".format(iothub_device.device_etag))
    print("tags                           = {0}".format(iothub_device.tags))
    print("version                        = {0}".format(iothub_device.version))

    print("status                         = {0}".format(iothub_device.status))
    print("status_reason                  = {0}".format(iothub_device.status_reason))
    print("status_update_time             = {0}".format(iothub_device.status_update_time))
    print("connection_state               = {0}".format(iothub_device.connection_state))
    print("last_activity_time             = {0}".format(iothub_device.last_activity_time))
    print(
        "cloud_to_device_message_count  = {0}".format(iothub_device.cloud_to_device_message_count)
    )
    print("device_scope                   = {0}".format(iothub_device.device_scope))

    print("properties                     = {0}".format(iothub_device.properties))
    print("additional_properties          = {0}".format(iothub_device.additional_properties))
    print("")

def print_query_result(title, query_result):
    print("")
    print("Type: {0}".format(query_result.type))
    print("Continuation token: {0}".format(query_result.continuation_token))
    if query_result.items:
        x = 1
        for d in query_result.items:
            print_twin("{0}: {1}".format(title, x), d)
            x += 1
    else:
        print("No item found")

def iothub_service_sample_run():
    try:
        arduino_id = "AR01"
        desired_humid = 80
        desired_temp = 20
        iothub_registry_manager = IoTHubRegistryManager(IOTHUB_CONNECTION_STRING)
        desired_parameters = get_desired_data(arduino_id, desired_humid, desired_temp)
        print(desired_parameters)
        #Đoạn code dùng để patch twin vào cho client bên người dùng
        #B1: lấy ra twin từ thiết bị
        twin = iothub_registry_manager.get_twin(DEVICE_ID)
        #B2: khởi tạo twin, lưu ý, chỉ có thể thêm vào tags twin và desired twin !
        twin_patch = Twin(properties = TwinProperties(desired = desired_parameters))
        twin = iothub_registry_manager.update_twin(DEVICE_ID, twin_patch, twin.etag)

        # Add a delay to account for any latency before executing the query
        sleep(1)

        #Query về để xử lý !
        sql = "SELECT * FROM devices WHERE deviceId = 'demorasberry'"
        query_spec = QuerySpecification(query= sql)
        query_result = iothub_registry_manager.query_iot_hub(query_spec, None, 100)
        #print("Devices in Hanoi plant: {}".format(', '.join([twin.device_id for twin in query_result.items])))
        print_query_result("Demo Rasberrypi device twin" ,query_result)
        
        #In reported parameters
        d = query_result.items[0]
        sensor_data = d.properties.reported
        print("Arduino sensor data {0}: ".format(arduino_id))
        print("Humidity = {0}".format(sensor_data['SensorParameters'][arduino_id]['Humidity']))
        print("Temperature = {0}".format(sensor_data['SensorParameters'][arduino_id]['Temperature']))
        
        #sleep(1)
        # query_spec = QuerySpecification(query="SELECT * FROM devices WHERE tags.location.plant = 'Hanoi' AND properties.reported.connectivity = 'cellular'")
        # query_result = iothub_registry_manager.query_iot_hub(query_spec, None, 100)
        # print("Devices in Redmond43 plant using cellular network: {}".format(', '.join([twin.device_id for twin in query_result.items])))

    except Exception as ex:
        print("Unexpected error {0}".format(ex))
        return
    except KeyboardInterrupt:
        print("IoT Hub Device Twin service sample stopped")
    finally:
        print("Shutting down")

if __name__ == '__main__':
    print("Starting the Python IoT Hub Device Twin service sample...")
    print()
    iothub_service_sample_run()