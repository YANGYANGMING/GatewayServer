import os, django, time, threading, random
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GatewayServer.settings")
django.setup()

from datetime import datetime
from GWS import models

# a = {'id': 1, 'sensor_id': '536876188', 'network_id': '0.0.0.1', 'alias': '1号传感器sd', 'received_time_data': "{'month': '*', 'day': '*', 'hour': '1', 'mins': '1'}", 'cHz': '2', 'gain': '60', 'avg_time': '4', 'Hz': '2', 'Sample_depth': '2', 'Sample_Hz': '500', 'sensor_type': 0, 'Importance': 0, 'date_of_installation': '2020-3-25', 'initial_thickness': '10.0', 'alarm_thickness': '8.0', 'alarm_battery': '50', 'area': '一区', 'location': '1号出料管道处', 'location_img_path': '', 'description': '1号出料管道腐蚀测量', 'assembly_crewman': 'yyy'}
# models.Sensor.objects.filter(sensor_id=a['sensor_id']).update(**a)
# last_sample_time = models.Waveforms.objects.filter(sensor_id='536876189').values('sensor_id', 'time_tamp').last()
# print(last_sample_time)

# data = {'received_time_data': {'month': '*', 'day': '*', 'hour': '12', 'mins': '0'}, 'sensor_id': '536876189', 'alias': '2号传感器', 'network_id': '0.0.1.2', 'sensor_type': '0', 'Importance': '0', 'initial_thickness': '10', 'alarm_thickness': '8', 'alarm_battery': '60', 'area': 'dffg', 'location': 'fdgdf', 'assembly_crewman': 'yyy', 'description': 'fdgf'}
# models.Sensor.objects.create(**data)
# sensor_obj_list = models.Sensor.objects.filter(gateway__network_id='0.0.1.0', delete_status=0)
# print(sensor_obj_list)
# sensor_list = sensor_obj_list.values('sensor_id', 'network_id', 'received_time_data', 'alias', 'battery',
#                                      'location', 'date_of_installation', 'sensor_run_status', 'sensor_online_status ',
#                                      'sensor_type', 'Importance')
# print(sensor_list)

# test_data = {'com_version': 'emat_com 0.1', 'network_id': ntid_obj, 'temperature': -999, 'gain': 60, 'battery': 100, 'data_len': 2048, 'data': [1641, 1653, 1243], 'time_tamp': '2020-03-26 08:47:42', 'thickness': 9.352}
#
# models.Waveforms.objects.create(**test_data)
# user_obj = models.UserProfile.objects.filter(name='root').first()
# gateway_obj = user_obj.gateway.all()
# print(gateway_obj)
# for gw_item in gateway_obj:
#     sensor_count = models.Sensor.objects.filter(gateway=gw_item).count()
# from datetime import datetime
# i = 1
# data_latest = models.Waveforms.objects.filter(network_id='0.0.1.10').values('time_tamp', 'thickness').last()
#
# latest_thickness = data_latest['thickness']
# print(latest_thickness)
# while latest_thickness == 0:
#     data_latest = models.Waveforms.objects.filter(network_id='0.0.1.10').values('time_tamp', 'thickness').order_by('-id')[int('%s' % i)]
#     latest_thickness = data_latest['thickness']
#     i += 1
#     print(latest_thickness)

# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.linear_model import LinearRegression
#
# a = [0, 0.87229167, 1.92459491, 2.92549769, 3.92738426, 4.92836806, 5.95005787, 6.95111111, 7.95231481,   8.95377315, 9.95532407, 10.95608796, 12.96086806, 13.79961806, 14.80265046, 15.80413194, 16.83905093, 18.85353009, 19.85394676, 20.85523148, 21.85631944, 22.85665509, 23.85744213, 24.85819444, 25.85846065, 25.8587963]
# b = [9.52,  9.522, 9.519, 9.522, 9.521, 9.518, 9.516, 9.518, 9.521, 9.517, 9.517, 9.516, 9.515, 9.518, 9.515, 9.515, 9.516, 9.517, 9.516, 9.513, 9.51,  9.513, 9.512, 9.51, 9.509, 9.51 ]
# print(len(a))
# print(len(b))
#
# x = np.array(a)
# y = np.array(b)
#
# def skl_func():
#     lr = LinearRegression()
#     lr.fit(x.reshape(-1, 1), y)
#     y_hat = lr.predict(np.arange(0, 30, 0.75).reshape(-1, 1))
#     print('skl_func:\tW = %f\n\tb = %f' % (lr.coef_, lr.intercept_))
#     plt.scatter(x, y)
#     plt.plot(np.arange(0, 30, 0.75), y_hat, color='g', marker='x', label='skl_func')
#
#
# skl_func()
# plt.legend(loc='upper left')
# plt.show()

# cur_company = models.Sensor.objects.values('gateway__Enterprise').filter(network_id='0.0.1.2')[0][
#     'gateway__Enterprise']
#
# db_time_obj = models.Sensor.objects.filter(gateway__Enterprise=cur_company).values('received_time_data')
# db_time_list = []
# for item in db_time_obj:
#     db_time_list.append(eval(item['received_time_data']))
# print(db_time_list)

# from queue import PriorityQueue
# from pypinyin import lazy_pinyin
# dic = {}
# generate_queue = locals()
# network_id = '0.0.2.1'
# Enterprise = '中石油'
# level = 2
# HZ_Enterprisea_name = lazy_pinyin(Enterprise)
# # queue_variable_name = "".join((str(i) for i in HZ_Enterprisea_name))
# queue_variable_name = ['zhongshiyou', 'zhongshihua']
# for item in queue_variable_name:
#     if not generate_queue.get(item):
#         generate_queue[item] = PriorityQueue()
#     queue_variable = generate_queue.get(item)
#     # 把network_id加入队列
#     queue_variable.put((level, item))
#     dic[item] = queue_variable
#     # print(queue_variable)
# # print(generate_queue)
# # print(generate_queue['queue_variable_name'])
# # print(dic)
# print(dic['zhongshiyou'].get())



# # product and consumer model
# pq = PriorityQueue()
# def Product():
#     count = 0
#     while True:
#         time.sleep(5)
#         pq.put((1, count))
#         print('已经put了%s\n' % count)
#         count += 1
#
#
# def Consumer(name):
#     count = 0
#     while True:
#         time.sleep(random.randrange(4))
#         data = pq.get()
#         print('%s get ' % name, data)
#         count += 1
#
#
# p1 = threading.Thread(target=Product)
# c1 = threading.Thread(target=Consumer, args=("AAA", ))
# c2 = threading.Thread(target=Consumer, args=("BBB", ))
#
# p1.start()
# c1.start()
# c2.start()





