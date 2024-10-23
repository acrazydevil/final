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
address_api = '/home/a/Desktop/Thouzer-Basic-main/cir/mqtt_api'

# Connect to MQTT server
def mqtt_connect():
    mqttClient.username_pw_set(username, password)  # MQTT Server PW
    mqttClient.connect(ip, port, 60)
    mqttClient.loop_start()
    print('Connect Sucessfully')

def open_json(n):
    if n == 0 :
        with open(address_api + '/moving_forward_no_obstacles.json', 'r') as read_file :
            api = json.load(read_file)
    elif n == 1 :
        with open(address_api + '/moving_30_no_obstacles.json', 'r') as read_file :
            api = json.load(read_file)
    elif n == 2 :
        with open(address_api + '/moving_-30_no_obstacles.json', 'r') as read_file :
            api = json.load(read_file)
    elif n == 3 :
        with open(address_api + '/moving_backward_no_obstacles.json', 'r') as read_file :
            api = json.load(read_file)
    elif n == 4 :
        with open(address_api + '/obstacle_avoiding_running.json', 'r') as read_file :
            api = json.load(read_file)      
    elif n == 5 :
        with open(address_api + '/arc_curve_running.json', 'r') as read_file :
            api = json.load(read_file)    
    return api
    
def on_publish(n):
    msg = str(open_json(n))
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
    while True :
        n = input("please enter number (0 ~ 3) ")
        n = int(n)
        # mqtt_connect()
        if 0 <= n <= 5 :
            mqtt_connect()
            on_publish(n)
        else :
            print("Please enter right number (0 ~ 3) ")
            break
        break
    
root.mainloop()


