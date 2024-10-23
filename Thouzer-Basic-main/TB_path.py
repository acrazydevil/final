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

topic_pub = '0/THOUZER_HW/RMS-10B1-AAJ65/exec/cmd'
address_api = '/home/a/Desktop/Thouzer-Basic-main/cir/mqtt_api'

# Connect to MQTT server
def mqtt_connect():
    mqttClient.username_pw_set(username, password)  # MQTT Server PW
    mqttClient.connect(ip, port, 60)
    mqttClient.loop_start()
    # print('Connect Sucessfully')

def open_json():
    with open(address_api + '/MT_MemorizeMode.json', 'r') as read_file:
        api = json.load(read_file)
    return api
    
def on_publish():
    msg = str(open_json())
    msg = msg.replace("'",'"')
    # print(msg)
    mqttClient.publish(topic_pub, f'{msg}')

params = {}
def on_message_come(client, userdata, msg):       
    global params
    _str = str(msg.payload.decode('gb2312'))
    params = json.loads(_str)
    # print('Topic: ' + msg.topic + ', Message: ' + str(msg.payload.decode('gb2312')))

if __name__ == '__main__':
    mqtt_connect()
    on_publish()

root.mainloop()

