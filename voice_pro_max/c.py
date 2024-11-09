from flask import Flask, render_template, jsonify,request
import speech_recognition as sr
from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger
import soundfile
import time
import json
from paho.mqtt import client as mqtt
import roslibpy

app = Flask(__name__,static_url_path='/static')

client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
mqttClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,client_id)

# IP & Port of Thouzer Basic
ip = '192.168.212.1'
port = 1883

# Username & Password of Thouzer Basic
username = 'SmartRobot'
password = 'SmartRobot'

topic_pub = '0/THOUZER_HW/RMS-10B1-AAJ65/exec/cmd'
address_api = '/home/wen/Desktop/voice_pro_max/mqtt_api'
topic_sub='0/THOUZER_HW/RMS-10B1-AAJ65/event/app'


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
            with open(address_api + '/MT_MemorizeMode.json', 'r') as read_file :
                api = json.load(read_file)
        elif n == 2 :
            with open(address_api + '/pub_MT_700.json', 'r') as read_file :
                api = json.load(read_file)
        elif n == 3:
            with open(address_api + '/pub_MT_701.json', 'r') as read_file :
                api = json.load(read_file)
        return api

def on_publish_start():
        msg = str(start_motion_json())
        msg = msg.replace("'",'"')
        # print(msg)
        mqttClient.publish(topic_pub, f'{msg}')

def on_publish(n):
        msg = str(open_json(n))
        msg = msg.replace("'",'"')
        # print(msg)
        mqttClient.publish(topic_pub, f'{msg}')


def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    status=payload['data']['status']
    if payload['data']['status']=='success':
        listener.publish(roslibpy.Message({'data':status}))
    # print("[{}]: {}".format(msg.topic, str(msg.payload)))

def mqtt_on_connect(client, userdata, flags, rc) :
    if rc == 0 :
        # print('Connect to MQTT Broker')
        mqttClient.subscribe(topic_sub)
    else :
        print('Connect failed')
    
def callback(message):
    mqtt_connect()
    on_publish_start()
    time.sleep(1.5)
    on_publish(3)
    # print('{}'.format(message['data']))
    # print(555)

# 路由函数，用于执行语音识别和关键字提取
@app.route('/execute_speech_recognition', methods=['POST'])
def execute_speech_recognition():
    global n
    audio_file = request.files['audio']
    data, samplerate = soundfile.read(audio_file)

    soundfile.write('received_audio.wav', data, samplerate, subtype='PCM_16')
    r = sr.Recognizer()

    with sr.AudioFile('received_audio.wav') as source:
        audio = r.record(source)  

    try:
        text = r.recognize_google(audio, language='zh-TW')
        print("您說的是：" + text)
    except sr.UnknownValueError:
        print("無法識別語音")
    except sr.RequestError as e:
        print("無法取得語音識別服務；{0}".format(e))
    
    ws_driver = CkipWordSegmenter(model="bert-base")
    pos_driver = CkipPosTagger(model="bert-base")
    ws = ws_driver([text])
    pos = pos_driver(ws)

    def pack_ws_pos_sentence(sentence_ws, sentence_pos):
        assert len(sentence_ws) == len(sentence_pos)
        res = []
        for word_ws, word_pos in zip(sentence_ws, sentence_pos): 
            res.append(f"{word_ws}({word_pos})")
        return "\u3000".join(res)

    def extract_keywords(sentence_ws, sentence_pos, pos_tags):
        keywords = []
        for word_ws, word_pos in zip(sentence_ws, sentence_pos):
            # 只保留名詞和動詞作為關鍵字
            if word_pos in pos_tags:
                keywords.append(word_ws)
        return keywords

    for sentence, sentence_ws, sentence_pos,in zip([text], ws, pos):
        print(sentence)
        print(pack_ws_pos_sentence(sentence_ws, sentence_pos))
        # 提取名詞和動詞作為關鍵字
        place = extract_keywords(sentence_ws, sentence_pos, ['Nc'])
        things = extract_keywords(sentence_ws, sentence_pos, ['Na'])
    print(place,things)
    result = {
            'text': text,
            'place': place,
            'things':things
    }

    #===========================================================================

    mqtt_connect()
    on_publish_start()
    time.sleep(1.5)
    if text[0:4]=='路線規劃':
        on_publish(1)
    elif place[0]=='實驗室':
        on_publish(2)
    elif place[0]=='辦公室':
        on_publish(3)
    # on_subscribe()
    return jsonify(result)

# 主页路由
@app.route('/')
def index():
    return render_template('index1.html')

if __name__ == '__main__':
    client = roslibpy.Ros(host='localhost', port=9090)
    client.run()
    listener=roslibpy.Topic(client,'/amr_arm_com','/std_msgs/String')
    listener2=roslibpy.Topic(client,'/amr_arm_com2','/std_msgs/String')
    listener2.subscribe(callback)
    app.run(debug=True, port=5000)

#ngrok http --domain=hip-roughly-falcon.ngrok-free.app localhost:5000
#roslaunch rosbridge_server rosbridge_websocket.launch
#rosrun tf2_web_republisher tf2_web_republisher