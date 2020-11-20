import os, django, time, threading, random, json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GatewayServer.settings")
django.setup()

from datetime import datetime
from GWS import models
from queue import PriorityQueue

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
# pq = PriorityQueue()
# pq.put((0, 'q'))
# pq.put((-1, 'w'))
# print(pq.get())
# print(pq.get())

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

# interval_val = 0.03
#
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

# def struct_to_stamp(struct):
#     timeArray = time.strptime(struct, "%Y-%m-%d %H:%M:%S")
#     timeStamp = int(time.mktime(timeArray))
#     return timeStamp
#
#
# def stamp_to_struct(stamp):
#     timeArray = time.localtime(stamp)
#     struct_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
#     return struct_time
#
#
# latest_vals = models.Waveforms.objects.values('thickness', 'temperature', 'battery', 'time_tamp').filter(
#     network_id='0.0.2.5')
#
# alarm_stamp_time = struct_to_stamp(latest_vals.last()['time_tamp']) + 600
# alarm_struct_time = stamp_to_struct(alarm_stamp_time)

# from django.db.models import Q
#
# search_key = "1号传感器 2020-08-06"
# querysets = models.Waveforms.objects.values('id', 'network_id__network_id', 'network_id__alias', 'battery',
#                                                     'time_tamp', 'thickness', 'temperature').all()
# def query_filter(search_key, querysets):
#     q = Q()
#     q.connector = "OR"
#     filter_field = ['network_id__network_id', 'network_id__alias', 'time_tamp', 'temperature', 'battery',
#                     'thickness']
#     search_key = search_key.split(' ')
#     for filter_item in filter_field:
#         for search_key_item in search_key:
#             # q.children.append(("%s__contains" % filter_item, search_key))
#             # test = querysets.filter(Q(filter_item__contains=search_key_item) & Q(publish_date__year=2018))
#             test = querysets.filter(Q(network_id__alias__contains='1号传感器') & Q(time_tamp__contains='2020-08-06'))
#
#     print(q)
#     print(type(q))
#     result = querysets.filter(q)
#
#     return result
#
# result = query_filter(search_key, querysets)
# print(result)

# days_interval = 7
# days_interval_time_stamp = (days_interval - 1) * 24 * 60 * 60
# latest_struct_time = models.Waveforms.objects.filter(network_id='0.0.2.1').values('time_tamp', 'thickness').order_by('-id').first()
# print(latest_struct_time['time_tamp'])
# latest_stamp_time = datetime.strptime(latest_struct_time['time_tamp'], "%Y-%m-%d %H:%M:%S").timestamp()
# first_stamp_time = latest_stamp_time - days_interval_time_stamp
# timeArray = time.localtime(first_stamp_time)
# first_struct_time = time.strftime("%Y-%m-%d", timeArray)
# print(first_struct_time)
# data_list = models.Waveforms.objects.filter(network_id='0.0.2.1',
#                                             time_tamp__gte=first_struct_time,
#                                             time_tamp__lte=latest_struct_time,
#                                             ).values('time_tamp', 'thickness')
# print(data_list)
# print(data_list.count())

# print(datetime.strptime("2020-07-30 00:00:00", "%Y-%m-%d %H:%M:%S").timestamp() * 1000)
# print(1598745600000)
#
# timeArray = time.localtime(1598745600)
# otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
# print(otherStyleTime)


# from django.contrib.auth.models import Group, Permission
# group_obj = Group.objects.get(id=2)
# print(group_obj)
# permissions_list = group_obj.permissions.values('id')
# print(permissions_list)


# import struct
# a = 2000000000
# data_length = struct.pack('i', a)
# print(data_length)
# print(len(data_length))
# length = struct.unpack('i', data_length)[0]
# print(length)


# from utils.handle_func import handle_data_to_send_administration
# from utils.socket_client import mysocket
# data = {
#     'network_id': "0.0.2.1",
#     'temperature': 156,
#     'thickness': 10.203,
# }
#
# send_data = handle_data_to_send_administration(method='UPDATA', data=data)
# recv_response = mysocket(send_data)
# print(recv_response)


# import hashlib

# message = b"Hello"

# md_obj = hashlib.md5()
# md_obj.update(message)
# md5_val = md_obj.hexdigest()
# print(md5_val)


# from gmssl import sm2, sm3, func
# from utils.socket_client import UPLOAD_DATA


# uid_len = 0x0080
# uid = 0x31323334353637383132333435363738
# a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
# b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
# xG = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
# yG = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
# xA = 0xD69C2F1EEC3BFB6B95B30C28085C77B125D77A9C39525D8190768F37D6B205B5
# yA = 0x89DCD316BBE7D89A9DC21917F17799E698531F5E6E3E10BD31370B259C3F81C3
# n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
# p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
# print(sm3.sm3_hash(str(uid_len + uid + a + b + xG + yG + xA + yA)))
# string = str(uid_len + uid + a + b + xG + yG + xA + yA)
# print(string)
# out1 = SM3(string).hash
# print(out1)
# print(len(out1))

# hex1 = '1c56'
# hex2 = '1d'
# dec1 = eval(hex1)
# dec2 = eval(hex2)
# bin1 = '{:b}'.format(dec1)
# bin2 = '{:b}'.format(dec2)
# print(bin1)
# print(bin2)
# print(bin1 + bin2)

# import binascii
#
# def str_to_hexStr(string):
#     str_bin = string.encode('utf-8')
#     return binascii.hexlify(str_bin).decode('utf-8')

# # # hash uid + params
# h256 = str(uid_len)[2:] + str(uid)[2:] + str(a)[2:] + str(b)[2:] + str(xG)[2:] + str(yG)[2:] + str(xA)[2:] + str(yA)[2:]
# uid_and_params_hash = sm3.sm3_hash(func.bytes_to_list(bytes(h256, encoding='utf-8')))
# print('uid_and_params_hash==', uid_and_params_hash)
# # print('uid_and_params_hash==', len(uid_and_params_hash))
#
# # # hash u / p + data
# hex_UPLOAD_DATA = str_to_hexStr(json.dumps(UPLOAD_DATA))
# uid_and_params_and_data_hash = sm3.sm3_hash(func.bytes_to_list(bytes(uid_and_params_hash + hex_UPLOAD_DATA, encoding='utf-8')))
# # print('uid_and_params_and_data_hash_hex==', uid_and_params_and_data_hash)
# # print('uid_and_params_and_data_hash_hex==', len(uid_and_params_and_data_hash))
# # print('uid_and_params_and_data_hash_int==', int(uid_and_params_and_data_hash, 16))
#
# # # generate keys
# # def is_on_curve(point):
# #     """如果给定点位于椭圆曲线上，则返回True。"""
# #     if point is None:
# #         # None represents the point at infinity.
# #         return True
# #
# #     x, y = point
# #
# #     return (y * y - x * x * x - a * x - b) % p == 0
# # def point_neg(point):
# #     """返回-点。"""
# #     assert is_on_curve(point)
# #
# #     if point is None:
# #         # -0 = 0
# #         return None
# #
# #     x, y = point
# #     result = (x, -y % p)
# #
# #     assert is_on_curve(result)
# #
# #     return result
# # def inverse_mod(k, p):
# #     """ 返回k模p的逆。
# #         此函数只返回（x*k）%p==1的整数x。
# #         k必须非零，p必须是素数。
# #     """
# #     if k == 0:
# #         raise ZeroDivisionError('division by zero')
# #
# #     if k < 0:
# #         # k ** -1 = p - (-k) ** -1  (mod p)
# #         return p - inverse_mod(-k, p)
# #
# #     # Extended Euclidean algorithm.
# #     s, old_s = 0, 1
# #     t, old_t = 1, 0
# #     r, old_r = p, k
# #
# #     while r != 0:
# #         quotient = old_r // r
# #         old_r, r = r, old_r - quotient * r
# #         old_s, s = s, old_s - quotient * s
# #         old_t, t = t, old_t - quotient * t
# #
# #     gcd, x, y = old_r, old_s, old_t
# #
# #     assert gcd == 1
# #     assert (k * x) % p == 1
# #
# #     return x % p
# # def point_add(point1, point2):
# #     """根据分组法返回point1+point2的结果。"""
# #     assert is_on_curve(point1)
# #     assert is_on_curve(point2)
# #
# #     if point1 is None:
# #         # 0 + point2 = point2
# #         return point2
# #     if point2 is None:
# #         # point1 + 0 = point1
# #         return point1
# #
# #     x1, y1 = point1
# #     x2, y2 = point2
# #
# #     if x1 == x2 and y1 != y2:
# #         # point1 + (-point1) = 0
# #         return None
# #
# #     if x1 == x2:
# #         # This is the case point1 == point2.
# #         m = (3 * x1 * x1 + a) * inverse_mod(2 * y1, p)
# #     else:
# #         # This is the case point1 != point2.
# #         m = (y1 - y2) * inverse_mod(x1 - x2, p)
# #
# #     x3 = m * m - x1 - x2
# #     y3 = y1 + m * (x3 - x1)
# #     result = (x3 % p,
# #               -y3 % p)
# #
# #     assert is_on_curve(result)
# #
# #     return result
# # def scalar_mult(k, point):
# #     """返回使用double和point_add算法计算的k*点。"""
# #     assert is_on_curve(point)
# #
# #     if k % n == 0 or point is None:
# #         return None
# #
# #     if k < 0:
# #         # k * point = -k * (-point)
# #         return scalar_mult(-k, point_neg(point))
# #
# #     result = None
# #     addend = point
# #
# #     while k:
# #         if k & 1:
# #             # Add.
# #             result = point_add(result, addend)
# #
# #         # Double.
# #         addend = point_add(addend, addend)
# #
# #         k >>= 1
# #
# #     assert is_on_curve(result)
# #
# #     return result
# # def make_keypair():
# #     """生成随机的私钥对。"""
# #     private_key = random.randrange(1, n)
# #     public_key = scalar_mult(private_key, (xG, yG))
# #     # print('public_key==', public_key)
# #     # print('public_key_len', len(public_key))
# #     return private_key, public_key
# # private, public = make_keypair()
# # print("Private key:", hex(private))
# # print("Public key: (0x{:x}, 0x{:x})".format(*public))
#
# # # sign
# private = '191421ea268b74310a37963b60c2735884c6cc6bdc92f5be2001464393d2d102'
# public = ('6857d626cf9b286efdb762cdb79ad10ebf207b0df96ac6e8eb7318cf7bffeccf', '49fb5148ccfb3efe3869d5493450f4a4544a88c0ffc3a7f71d418f66ced64fe0')
# sm2_crypt = sm2.CryptSM2(public_key=public, private_key=private)
# random_hex_str = func.random_hex(sm2_crypt.para_len)
# print('random_hex_str', random_hex_str)
# sign = sm2_crypt.sign(uid_and_params_and_data_hash, random_hex_str)
# print(sign)  # 38c1d2e7d51d71c2e2a29e48c2edb37c0dc4d2b033a74c6f6e3f43ccaa71bc3f2d6f96890a1e42b09935b2ddbba23d5e56f98b46151c348c32f4fdb940121808


# # 解签
# sm2_crypt.verify(sign, uid_and_params_and_data_hash)

# user_obj_list = models.UserProfile.objects.values('id').filter(gateway__Enterprise="零声科技（苏州）有限公司", role__name="管理员")
# print(user_obj_list)

# with open('data_time.txt', 'r') as f:
#     while True:
#         data_time = f.readline()
#         if data_time:
#             print(data_time.strip('\n'))
#         else:
#             break
#
# models.Sensor.objects.filter(id=1).exists()


# data_obj = models.Waveforms.objects.values('network_id', 'data', 'time_tamp', 'gain', 'temperature', 'battery', 'thickness').filter(network_id='0.0.2.1', id__lte=1325)
# with open('false_data.txt', 'w') as f:
#     for item in data_obj:
#         f.write(item['network_id'] + '\t' + item['data'] + '\t' + item['time_tamp'] + '\t' + str(item['gain']) + '\t' + str(item['temperature']) + '\t' + str(item['battery']) + '\t' + str(item['thickness']) + '\n')
# print(data_obj.count())
# ntid_obj = models.Sensor.objects.get(network_id='0.0.1.1')
# with open('false_data.txt', 'r') as f:
#     for i in range(data_obj.count()):
#         datas = f.readline().strip('\n').split('\t')
#         data_dict = {'network_id': ntid_obj, 'data': datas[1], 'time_tamp': datas[2], 'gain': datas[3], 'temperature': datas[4], 'battery': datas[5], 'thickness': datas[6], 'data_len': 2048, 'com_version': 'emat_com 0.1'}
#         models.Waveforms.objects.create(**data_dict)

# with open('false_data.txt', 'r') as f:
#     with open('false_data2.txt', 'w') as f2:
#         for i in range(48):
#             data1 = f.readline().strip('\n').split('\t')
#             month = data1[2].replace('04', '07', 1)
#             data1[2] = month
#             new_data1 = '\t'.join(data1)
#             f2.write(new_data1 + '\n')
#         for i in range(48, 110):
#             data2 = f.readline().strip('\n').split('\t')
#             month = data2[2].replace('05', '08', 1)
#             data2[2] = month
#             new_data2 = '\t'.join(data2)
#             f2.write(new_data2 + '\n')
#         for i in range(110, 154):
#             data3 = f.readline().strip('\n').split('\t')
#             month = data3[2].replace('06', '09', 1)
#             data3[2] = month
#             new_data3 = '\t'.join(data3)
#             f2.write(new_data3 + '\n')