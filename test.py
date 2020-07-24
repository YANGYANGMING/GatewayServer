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


# print(random.uniform(-0.03, 0.01))
# print(round(0.0232, 3))

# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.linear_model import LinearRegression
#
# n = 101
#
# x = np.linspace(0, 10, n)
# noise = np.random.randn(n)
# y = 2.5 * x + 0.8 + 2.0 * noise
#
#
# def self_func(steps=100, alpha=0.01):
#     w = 0.5
#     b = 0
#     alpha = 0.01
#     for i in range(steps):
#         y_hat = w * x + b
#         dy = 2.0 * (y_hat - y)
#         dw = dy * x
#         db = dy
#         w = w - alpha * np.sum(dw) / n
#         b = b - alpha * np.sum(db) / n
#         e = np.sum((y_hat - y) ** 2) / n
#         # print (i,'W=',w,'\tb=',b,'\te=',e)
#     print('self_func:\tW =', w, '\n\tb =', b)
#     plt.scatter(x, y)
#     plt.plot(np.arange(0, 10, 1), w * np.arange(0, 10, 1) + b, color='r', marker='o',
#              label='self_func(steps=' + str(steps) + ', alpha=' + str(alpha) + ')')
#
#
# def skl_func():
#     lr = LinearRegression()
#     lr.fit(x.reshape(-1, 1), y)
#     y_hat = lr.predict(np.arange(0, 10, 0.75).reshape(-1, 1))
#     print('skl_fun:\tW = %f\n\tb = %f' % (lr.coef_, lr.intercept_))
#     plt.plot(np.arange(0, 10, 0.75), y_hat, color='g', marker='x', label='skl_func')
#
#
# self_func(10000)
# skl_func()
# plt.legend(loc='upper left')
# plt.show()

# # interval_val = 0.03
# #
# w_obj = list(models.Waveforms.objects.values('id').filter(network_id='0.0.2.1'))
# thickness = 10.087
# interval = 0.0005
# init = 0
# noise = (-0.002, 0.001)
# for item in w_obj:
#     new_thickness = round(thickness + random.uniform(-0.009, 0.009) - init, 3)
#     init += interval
#     # print(day, '：', thickness)
#     # day += 1
#
#     models.Waveforms.objects.filter(id=item['id']).update(thickness=new_thickness)
#     # models.Waveforms.objects.filter(id=item['id']).update(time_tamp=temp, thickness=round((10.02 + random.uniform(-0.03, 0.01)), 3))


# # 生成二维码
# import qrcode
# # 实例化二维码生成类
# qr = qrcode.QRCode(
#     version=1,
#     error_correction=qrcode.constants.ERROR_CORRECT_L,
#     box_size=10,
#     border=4,
# )
# # 设置二维码数据
# data = "https://www.baidu.com"
# qr.add_data(data=data)
#
# # 启用二维码颜色设置
# qr.make(fit=True)
# img = qr.make_image(fill_color="green", back_color="white")
#
# # 显示二维码
# img.show()

# from GatewayServer.settings import accessKeyId, accessSecret, TemplateCode
# from aliyunsdkcore.client import AcsClient
# from aliyunsdkcore.request import CommonRequest
# import json
#
#
# def send_sms(PhoneNumbers, code):
#     """
#     发送短信验证码
#     :param PhoneNumbers: 获取验证码的手机号
#     :return:
#     """
#     client = AcsClient(accessKeyId, accessSecret, 'cn-hangzhou')
#
#     request = CommonRequest()
#     request.set_accept_format('json')
#     request.set_domain('dysmsapi.aliyuncs.com')
#     request.set_method('POST')
#     request.set_protocol_type('https')  # https | http
#     request.set_version('2017-05-25')
#     request.set_action_name('SendSms')
#
#     request.add_query_param('RegionId', "cn-hangzhou")
#     request.add_query_param('PhoneNumbers', PhoneNumbers)
#     request.add_query_param('SignName', "ABC商城")
#     request.add_query_param('TemplateCode', TemplateCode)
#     request.add_query_param('TemplateParam', "{\"code\": %s}" % code)
#
#     response = client.do_action_with_exception(request)
#     print(json.loads(response))
#
#     return json.loads(response)
#
# send_sms('17706248840', "1234")

import random
print(random.randrange(10000, 99999))



