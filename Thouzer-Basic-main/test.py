import tkinter as tk
import time
import json
from paho.mqtt import client as mqtt
import speech_recognition as sr
from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger, CkipNerChunker
# IP & Port of Thouzer Basic
ip = '192.168.212.1'
port = 1883 

# Username & Password of Thouzer Basic
username = 'SmartRobot'
password = 'SmartRobot'

topic_pub = '0/WHISPERER/RMS-10B1-AAJ65/nav'
topic_pub1 = '0/THOUZER_HW/RMS-10B1-AAJ65/exec/cmd'
address_api = '/home/a/Desktop/Thouzer-Basic-main/cir/mqtt_api'

root = tk.Tk()
client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
mqttClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,client_id)

def rec():
    # Initialize speech recognizer
    r = sr.Recognizer()

    # Use the microphone as source for audio
    with sr.Microphone() as source:
        print("請開始說話...")
        audio = r.listen(source)

    # Recognize speech using Google Speech Recognition
    try:
        text = r.recognize_google(audio, language='zh-TW')
        print("您說的是：" + text)
    except sr.UnknownValueError:
        print("無法識別語音")
    except sr.RequestError as e:
        print("無法取得語音識別服務；{0}".format(e))

    # Initialize CKIP transformers
    ws_driver = CkipWordSegmenter(model="bert-base")
    pos_driver = CkipPosTagger(model="bert-base")
    ner_driver = CkipNerChunker(model="bert-base")

    # Perform word segmentation
    ws = ws_driver([text])
    # Perform part-of-speech tagging
    pos = pos_driver(ws)
    # Perform named entity recognition
    ner = ner_driver([text])

    # Pack word segmentation and part-of-speech results
    def pack_ws_pos_sentence(sentence_ws, sentence_pos):
        assert len(sentence_ws) == len(sentence_pos)
        res = []
        for word_ws, word_pos in zip(sentence_ws, sentence_pos):
            res.append(f"{word_ws}({word_pos})")
        return "\u3000".join(res)

    # Keyword extraction function
    def extract_keywords(sentence_ws, sentence_pos, pos_tags):
        keywords = []
        for word_ws, word_pos in zip(sentence_ws, sentence_pos):
            # 只保留名詞和動詞作為關鍵字
            if word_pos in pos_tags:
                keywords.append(word_ws)
        return keywords

    # Show results
    for sentence, sentence_ws, sentence_pos, in zip([text], ws, pos, ner):
        print(sentence)
        print(pack_ws_pos_sentence(sentence_ws, sentence_pos))
        # 提取名詞和動詞作為關鍵字
        place = extract_keywords(sentence_ws, sentence_pos, ['Nc'])
        things = extract_keywords(sentence_ws, sentence_pos, ['Na'])
    print("地點:", place[0],end="\n")
    print("顏色:", things[0],end="\n")
    return text

# Connect to MQTT server
def mqtt_connect():
    mqttClient.username_pw_set(username, password)  # MQTT Server PW
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
    elif n == 5 :
        with open(address_api + '/obstacle_avoiding_running.json', 'r') as read_file :
            api = json.load(read_file)      
    elif n == 6 :
        with open(address_api + '/arc_curve_running.json', 'r') as read_file :
            api = json.load(read_file)   
    # elif n == 7 :
    #     with open(address_api + '/MT_MemorizeMode.json', 'r') as read_file :
    #         api = json.load(read_file)
    # elif n == 8 :
    #     with open(address_api + '/pub_MT_700.json', 'r') as read_file :
    #         api = json.load(read_file)
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
params = {}
def on_message_come(client, userdata, msg):       
    global params
    _str = str(msg.payload.decode('gb2312'))
    params = json.loads(_str)
    # print('Topic: ' + msg.topic + ', Message: ' + str(msg.payload.decode('gb2312')))

if __name__ == '__main__':
    mqtt_connect()
    on_publish_start()
    a=rec()
    print(a)
    # if a=="往前走":
    #     on_publish(1)
    # else:
    #     on_publish(4)
    # while True :
    #     # n = int(input())
    #     if n!=100:
    #         mqtt_connect()
    #         on_publish(n)
    #     else :
    #         break
root.mainloop()
