import paho.mqtt.client as mqtt
import json


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe([('aaa', 2), ('pub', 2)])
    client.publish("chat", json.dumps("Hello,anyone!"))


# 接收到消息的回调方法
def on_message(client, userdata, msg):
    # print(msg.topic+":"+str(msg.payload.decode()))
    # print(msg.topic+":"+msg.payload.decode())
    payload = json.loads(msg.payload.decode())
    print(msg.topic + ":" + payload)


if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    HOST = "192.168.238.129"

    client.connect(HOST, 1883, 30)
    # client.loop_forever()

    client.loop_start()

    while True:
        str = input()
        if str:
            client.publish("pub", json.dumps(str))