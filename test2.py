import json
DATA = {
    "Current_T": "2020-8-3 13:18:28",
    "Sensor_Mac": "123-456-789",
    "Gauge_Cycle": "48:00:00",
    "Material_Type": "45",
    "Material_Temp": 35.00,
    "Environmental_Temp": 30.00,
    "Sound_Velocity": 3249.0,
    "Voltage": 6.0,
    "LIM_Voltage": 4.0,
    "Ultrasonic_Freq": 1000.0,
    "Time_Cycle": "72:00:00",
    "Status": True,
    "Thickness": [
        {"Sensor_NO": "10010001202008259009", "Thickness": 5.35},
    ]
}
# Digital_Signature = '00ea811841d6687fe4447438611e48a9ecd751b2184130a50498e0ad653cd4d597a8a0f5ab8c80342b562149fd77c0a6a87ba53c96e2baa41f040218170460d9'
# UPLOAD_DATA = {"Digital_Signature": Digital_Signature, "DATA": DATA}
#
# json_data = json.dumps(UPLOAD_DATA)
# print(json_data)

# response_data = {"RESPONSE_CODE": {
#                     "receive": 1,
#                     "analysis": 1,
#                     "operation": 2
#                 },
#                 "OPERATION_TYPE": "GET",
#                 "BODY": {
#                     "Current_T": "2020-8-3 13:18:28",
#                     "Sensor_Mac": "123-456-789",
#                     }
#             }

operation_choice = {
    '1': 'SET',
    '2': 'GET',
    '3': 'UPDATA',
    '4': 'CAL'
}


class HandleSocketOperation():
    def __init__(self):
        pass

    def GET(self, tcp_client, sensor_id, **params):
        print('GET.....................................')
        operation_ack_data = {
            "OPERATION_TYPE_ACK": 21,
            "Current_T": "2020-8-3 13:18:28",
            "Sensor_Mac": "123-456-789",
            "Gauge_Cycle": "48:00:00",
            "Sound_Velocity": 3249.0,
            "Voltage": 6.0,
            "LIM_Voltage": 4.0,
            "Ultrasonic_Freq": 10.0,
            "Time_Cycle": "72:00:00",
            "Total_Numbers": 100
        }
        json_data = json.dumps(operation_ack_data).encode('utf-8')
        print(params)
        print(type(params))
        print(json_data)
        print(tcp_client)
        print(sensor_id)

    def SET(self, tcp_client, sensor_id, **params):
        print('SET.....................................')
        print(params)
        print(type(params))
        print(tcp_client)
        print(sensor_id)
        Gauge_Cycle = params['Gauge_Cycle'].split(':')
        print('Gauge_Cycle', Gauge_Cycle)
        received_time_data = {'days': str(int(Gauge_Cycle[0]) // 24), 'hours': str(int(Gauge_Cycle[0]) % 24), 'minutes': Gauge_Cycle[1]}
        print('received_time_data', received_time_data)

    def UPDATA(self, tcp_client, sensor_id, **params):
        pass

    def CAL(self, tcp_client, sensor_id, **params):
        pass

operation_func_obj = HandleSocketOperation()

tcp_client = 'aaa'
sensor_id = '1010101010'
recv_list = [{'RESPONSE_CODE': {'receive': 1, 'analysis': 1, 'operation': 2}, 'OPERATION_TYPE': 'GET'},
             {"RESPONSE_CODE": {"receive": 1, "analysis": 1,"operation": 1}, "OPERATION_TYPE": "SET", "BODY": {"Gauge_Cycle":"50:12:12"}}
             ]

for i in recv_list:
    # recv_response = {'RESPONSE_CODE': {'receive': 1, 'analysis': 1, 'operation': 2}, 'OPERATION_TYPE': 'GET'}

    operation = i['RESPONSE_CODE'].get('operation', '0')
    operation_type = operation_choice[str(operation)]
    params = i.get('BODY', {})
    if operation == '0':
        break
    else:
        getattr(operation_func_obj, operation_type)(tcp_client, sensor_id, **params)

import os, django, time, threading, random, json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GatewayServer.settings")
django.setup()
from GWS import models
sensor_obj = models.Sensor.objects.values('received_time_data', 'material').get(sensor_id='10010001201906018002')
received_time_data = eval(sensor_obj['received_time_data'])
print(received_time_data)
Gauge_Cycle = str(int(received_time_data['days']) * 24 + int(received_time_data['hours'])) + ":00:00"
print(Gauge_Cycle)


# time_list = ['2020-09-22 15:43:50', '2020-09-22 15:04:27', '2020-09-22 13:52:08', '2020-09-22 13:49:48', '2020-09-22 13:42:50', '2020-09-22 13:37:00', '2020-09-22 13:36:35', '2020-09-22 13:35:28', '2020-09-22 13:34:57', '2020-09-22 13:07:01', '2020-09-22 09:14:59', '2020-09-22 08:45:44', '2020-09-22 08:44:17', '2020-09-22 08:33:35', '2020-09-21 20:18:15', '2020-09-21 14:48:13', '2020-09-21 14:41:07', '2020-09-21 14:30:05', '2020-09-21 14:18:12', '2020-09-21 08:25:59', '2020-09-21 08:24:11', '2020-09-21 08:23:19', '2020-09-21 08:18:13', '2020-09-21 07:48:12', '2020-09-21 06:48:13', '2020-09-21 06:18:13', '2020-09-21 05:48:13', '2020-09-21 05:18:13', '2020-09-21 04:48:13', '2020-09-21 04:18:13', '2020-09-21 03:48:13', '2020-09-21 03:18:13', '2020-09-21 02:48:12', '2020-09-21 02:18:13', '2020-09-21 01:48:12', '2020-09-21 01:18:13', '2020-09-21 00:48:12', '2020-09-21 00:18:13', '2020-09-20 23:18:13', '2020-09-20 22:48:12', '2020-09-20 22:18:13']
with open('deviation_data_new_liqiang.txt', 'r') as f:
    while True:
        data = f.readline()
        print(data.strip('\n'))
        if data == "":
            break

