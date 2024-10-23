
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

topic_pub = '0/WHISPERER/RMS-10B1-AAJ65/vel2D_DWO'
address_api = '/home/a/Desktop/Thouzer-Basic-main/cir/mqtt_api'

# Connect to MQTT server
def mqtt_connect():
    mqttClient.username_pw_set(username, password)  # MQTT Server PW
    mqttClient.on_connect = mqtt_on_connect
    mqttClient.on_message = on_message
    mqttClient.connect(ip, port, 60)
    mqttClient.loop_start()
    #print('Connect Sucessfully')

# 接收訊息（接收到 PUBLISH）的回呼函數
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    print(payload)
    #print("[{}]: {}".format(msg.topic, str(msg.payload)))

def mqtt_on_connect(client, userdata, flags, rc) :
    if rc == 0 :
        print('Connect to MQTT Broker')
        mqttClient.subscribe(topic_pub)
    else :
        print('Connect failed')

if __name__ == '__main__' :
    mqtt_connect()

root.mainloop()
