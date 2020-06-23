import paho.mqtt.client as mqtt
from utils import handle_func
from GatewayServer import settings
import json


class MQTT_Client(object):
    
    def __init__(self):
        self.sub_list = [('pub', 2)]
        # models.Gateway.objects.values('network_id').all()
        for i in range(1, 6):
            temp_sub = ('0.0.%s.0' % i, 2)
            self.sub_list.append(temp_sub)
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe
        # self.client.on_log = self.on_log
        self.client.tls_set(ca_certs=settings.ca_certs,
                            certfile=settings.certfile,
                            keyfile=settings.keyfile
                            )
        self.client.tls_insecure_set(True)
        self.client.connect(settings.MQTT_HOST, 8883, 30)
        # self.client.connect(settings.MQTT_HOST, 1883, 30)
        self.client.loop_start()
    
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        result, mid = self.client.subscribe(self.sub_list)

    # 接收到消息的回调方法
    def on_message(self, client, userdata, msg):
        payload = json.loads(msg.payload.decode())
        if payload['id'] == 'client':
            print('-----------------------------------------------------------------------------------')
            print('msg.topic', msg.topic)
            print('payload............', payload)
            handle_func.handle_recv_gwdata(payload)

    # 在断开连接时callback，打印消息主题和内容
    def on_disconnect(self, client, userdata, rc):
        print("Disconnection returned result:" + str(rc))

    # 在订阅获得服务器响应后，从为响应列表中删除该消息 id
    def on_subscribe(self, client, userdata, mid, granted_qos):
        print('订阅成功....')

    # def on_log(self, client, obj, level, string):
    #     print("Log:", string)


try:
    mqtt_client = MQTT_Client()
    client = mqtt_client.client
except Exception as e:
    print(e)
    client = None





