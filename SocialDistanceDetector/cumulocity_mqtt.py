import paho.mqtt.client as mqtt
import time, random, threading
import multiprocessing as mp
import json

with open('config.json') as file:
    json_data = json.load(file)
    # client, user and device details
    serverUrl = json_data['mqttServerUrl']
    clientId = json_data['clientId']
    device_name = json_data['device_name']
    tenant = json_data['tenant']
    username = json_data['username']
    password = json_data['password']

# task queue to overcome issue with paho when using multiple threads:
#   https://github.com/eclipse/paho.mqtt.python/issues/354
task_queue = mp.Queue()


# display all incoming messages
def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print(f" < received message  {payload}")

    # This is a sample payload received from Cumulocity, signalling a restart command
    if payload.startswith("510"):
        task_queue.put(perform_restart)

    # This is a sample payload received from Cumulocity, signalling a restart command
    if payload.startswith("511"):
        command = payload.split(',')[2]
        print('Command Message Received. The command is ' + command)
        task_queue.put(perform_command)


def perform_command():
    publish("s/us", "501,c8y_Command", wait_for_ack=True)
    time.sleep(1)
    publish("s/us", "503,c8y_Command,Command Success", wait_for_ack=True)


# simulate restart
def perform_restart():
    print("Simulating device restart...")
    publish("s/us", "501,c8y_Restart", wait_for_ack=True)

    print("...restarting...")
    time.sleep(1)

    publish("s/us", "503,c8y_Restart", wait_for_ack=True);
    print("...restart completed")


# send measurement followinfg the mqtt api described in the cheatsheet
def send_measurement(measurement):

    print("Sending Violations")
    publish("s/us", f"200,c8y_Violations,V,{measurement}")


# publish a message
def publish(topic, message, wait_for_ack=False):
    QoS = 2 if wait_for_ack else 0
    message_info = client.publish(topic, message, QoS)
    if wait_for_ack:
        print(f" > awaiting ACK for {message_info.mid}")
        message_info.wait_for_publish()
        print(f" < received ACK for {message_info.mid}")

# display all outgoing messages
def on_publish(client, userdata, mid):
    print(f" > published message: {mid}")

# main device loop
# def device_loop():
#     while True:
#         task_queue.put(send_measurement)
#         time.sleep(7)



# connect the client to Cumulocity IoT and register a device

client = mqtt.Client(clientId)
client.username_pw_set(tenant + "/" + username, password)
client.on_message = on_message
client.on_publish = on_publish

client.connect(serverUrl)
client.loop_start()

time.sleep(3)
# Registers the device as an agent, which enables iot to receive commands from cumulocity
publish("s/us", f"100,{device_name},c8y_MQTTDevice", wait_for_ack = True)

# adds extra data for the device, such as the serialNumber,hardwareModel and revision
publish("s/us", "110,S123456789,MQTT test model,Rev0.1")
#time.sleep(3)
publish("s/us", f"100,{device_name},c8y_MQTTDevice", wait_for_ack = True)

# the supported operations for this device, in this case it is c8y_Restart and c8y_Command , which allows for the device to be
# restarted and sent for other Commands

publish("s/us", "114,c8y_Restart,c8y_Command")

print("Device registered successfully!")

# subscribe to operations
client.subscribe("s/ds")

# device_loop_thread = threading.Thread(target=device_loop)
# device_loop_thread.daemon = True
# device_loop_thread.start()

# process all tasks on queue
# try:
#     while True:
#         task = task_queue.get()
#         task()
# except (KeyboardInterrupt, SystemExit):
#     print("Received keyboard interrupt, quitting ...")
#     exit(0)

