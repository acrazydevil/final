import tkinter as tk
import time
import json
from paho.mqtt import client as mqtt

root = tk.Tk()
client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
mqttClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,client_id)

# IP & Port of Thouzer Basic
ip = '192.168.212.1'
port = 1883 

# Username & Password of Thouzer Basic
username = 'SmartRobot'
password = 'SmartRobot'

topic_pub = '0/WHISPERER/RMS-10B1-AAJ65/nav'
topic_pub1 = '0/THOUZER_HW/RMS-10B1-AAJ65/exec/cmd'
address_api = '/home/a/Desktop/voice_pro_max/mqtt_api'
topic_sub= '0/THOUZER_HW/RMS-10B1-AAJ65/event/app'

# Connect to MQTT server
def mqtt_connect():
    mqttClient.username_pw_set(username, password)  # MQTT Server PW
    mqttClient.on_connect = mqtt_on_connect
    mqttClient.on_message = on_message
    mqttClient.connect(ip, port, 60)
    mqttClient.loop_start()
    # print('Connect Sucessfully')

def start_motion_json():
    with open(address_api + '/start_motion.json', 'r') as read_file :
        api = json.load(read_file)
    return api

def open_json(n):
    if n == 1 :
        with open(address_api + '/moving_forward_no_obstacles.json', 'r') as read_file :
            api = json.load(read_file)
    elif n == 2 :
        with open(address_api + '/moving_30_no_obstacles.json', 'r') as read_file :
            api = json.load(read_file)
    elif n == 3 :
        with open(address_api + '/moving_-30_no_obstacles.json', 'r') as read_file :
            api = json.load(read_file)
    elif n == 4 :
        with open(address_api + '/moving_backward_no_obstacles.json', 'r') as read_file :
            api = json.load(read_file) 
    elif n == 7 :
        with open(address_api + '/MT_MemorizeMode.json', 'r') as read_file :
            api = json.load(read_file)
    elif n == 8 :
        with open(address_api + '/pub_MT_702.json', 'r') as read_file :
            api = json.load(read_file)
    elif n == 9 :
        with open(address_api + '/pub_MT_703.json', 'r') as read_file :
            api = json.load(read_file)
    elif n == 10 :
        with open(address_api + '/cancel.json', 'r') as read_file :
            api = json.load(read_file)
    return api

def on_publish_start():
    msg = str(start_motion_json())
    msg = msg.replace("'",'"')
    # print(msg)
    mqttClient.publish(topic_pub1, f'{msg}')

def on_publish(n):
    msg = str(open_json(n))
    msg = msg.replace("'",'"')
    # print(msg)
    mqttClient.publish(topic_pub, f'{msg}')
    # mqttClient.publish(topic_pub1, f'{msg}')

def on_publish1(n):
    msg = str(open_json(n))
    msg = msg.replace("'",'"')
    # print(msg)
    mqttClient.publish(topic_pub1, f'{msg}')

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    print(payload['data']['status'])
    # print("[{}]: {}".format(msg.topic, str(msg.payload)))

def mqtt_on_connect(client, userdata, flags, rc) :
    if rc == 0 :
        # print('Connect to MQTT Broker')
        mqttClient.subscribe(topic_sub)
    else :
        print('Connect failed')

if __name__ == '__main__':
    mqtt_connect()
    on_publish_start()
    while True :
        # mqtt_connect()
        print(4000)
        n = int(input())
        if n<=4:
            # for i in range(100):
                on_publish(n)
                # time.sleep(0.02)
        elif n>4:
            on_publish1(n)
        else :
            break
root.mainloop()


