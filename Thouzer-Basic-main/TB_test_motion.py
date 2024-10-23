import tkinter as tk
import time
import json
from paho.mqtt import client as mqtt

root = tk.Tk()
client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
mqttClient = mqtt.Client(client_id)

# IP & Port of Thouzer Basic
ip = '192.168.212.1'
port = 1883 

# Username & Password of Thouzer Basic
username = 'SmartRobot'
password = 'SmartRobot'

topic_pub1 = '0/THOUZER_HW/RMS-10B1-AAJ65/exec/cmd'
topic_pub2 = '0/WHISPERER/RMS-10B1-AAJ65/nav'

address_api = '/home/a/Desktop/Thouzer-Basic-main/cir/mqtt_api'

# Connect to MQTT server
def mqtt_connect():
    mqttClient.username_pw_set(username, password)  # MQTT Server PW
    mqttClient.connect(ip, port, 60)
    mqttClient.loop_start()
    # print('Connect Sucessfully')

def open_json1():
    with open(address_api + '/start_motion.json', 'r') as read_file :
        api = json.load(read_file)
    return api

def open_json2():
    with open(address_api + '/moving_forward_with_obstacles.json', 'r') as read_file :
        api = json.load(read_file)
    return api

def open_json3():
    with open(address_api + '/mode_cancel.json', 'r') as read_file :
        api = json.load(read_file)
    return api
    
def on_publish1():
    msg = str(open_json1())
    msg = msg.replace("'",'"')
    print(msg)
    mqttClient.publish(topic_pub1, f'{msg}')

def on_publish2():
    msg = str(open_json2())
    msg = msg.replace("'",'"')
    print(msg)
    mqttClient.publish(topic_pub2, f'{msg}')

def on_publish3():
    msg = str(open_json3())
    msg = msg.replace("'",'"')
    print(msg)
    mqttClient.publish(topic_pub1, f'{msg}')

params = {}
def on_message_come(client, userdata, msg):       
    global params
    _str = str(msg.payload.decode('gb2312'))
    params = json.loads(_str)
    #print('Topic: ' + msg.topic + ', Message: ' + str(msg.payload.decode('gb2312')))

if __name__ == '__main__':
    mqtt_connect()
    on_publish1()
    on_publish2()
    #on_publish3()
    
root.mainloop()


