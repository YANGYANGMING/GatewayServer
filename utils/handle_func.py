import json
import os
import time
import threading
from functools import reduce
from GWS import models
from GWS.views import views
from utils.mqtt_client import client
from datetime import datetime
import numpy as np
from sklearn.linear_model import LinearRegression
from PIL import Image
from queue import PriorityQueue
from pypinyin import lazy_pinyin


# views视图需要用到的返回数据值
update_gw_payload = {}
add_gw_payload = {}
recv_gwdata_payload = {}
pause_payload = {}
resume_payload = {}

generate_queue = locals()


class HandleFunc(object):

    def __init__(self):
        pass

    def sync_sensors(self, payload):
        """
        网关上电同步传感器
        :param payload:
        :return:GWS_sensor
        """
        sync_sensors = payload['sync_sensors']
        gateway_obj = models.Gateway.objects.filter(network_id=sync_sensors[0]['gateway']).first()
        server_network_id_dict = models.Sensor.objects.values('network_id').filter(gateway__network_id=sync_sensors[0]['gateway'])
        server_network_id_list = [item['network_id'] for item in server_network_id_dict]
        for item in sync_sensors:
            item['gateway'] = gateway_obj
            # update
            if item['network_id'] in server_network_id_list:
                models.Sensor.objects.filter(network_id=item['network_id']).update(**item)
                print('update')
                server_network_id_list.remove(item['network_id'])
            # create
            else:
                models.Sensor.objects.create(**item)
                print('create')
        # remove
        # print('server_network_id_list', server_network_id_list)
        if server_network_id_list:
            for remove_item in server_network_id_list:
                models.Sensor.objects.filter(network_id=remove_item).delete()
                print('remove')
        # Log
        views.log.log(payload['status'], payload['msg'], sync_sensors[0]['gateway'])

    def heart_ping(self, payload):
        """
        根据心跳更新网关状态
        :param payload:
        :return:
        """
        gwntid = payload['gwntid']
        models.Gateway.objects.filter(network_id=gwntid).update(gw_status=1)

    def connect_status(self, payload):
        """
        网关连接状态
        :param payload:
        :return:
        """
        models.Gateway.objects.filter(network_id=payload['gw_network_id']).update(gw_status=1)

    def update_sensor(self, payload):
        """
        接收到网关的数据进行更新传感器
        :return:
        """
        print('更新.........')
        if payload['status']:
            location_img_json = payload['receive_data'].pop('location_img_json')
            if location_img_json:
                location_img_path_and_name = payload['receive_data']['location_img_path']
                location_img_path = location_img_path_and_name.rsplit('/', 1)[0] + '/'
                # 判断是否存在路径
                mkdir_path(path=location_img_path)
                location_img_bytes = eval(json.loads(location_img_json.strip('\r\n')))
                print('location_img_path_and_name == ', location_img_path_and_name)
                with open(location_img_path_and_name, 'wb') as f:
                    f.write(location_img_bytes)
            models.Sensor.objects.filter(network_id=payload['receive_data']['network_id']).update(
                **payload['receive_data'])
        # Log
        views.log.log(payload['status'], payload['msg'], payload['receive_data']['network_id'], payload['user'])

    def add_sensor(self, payload):
        """
        接收到网关的数据进行增加传感器
        :return:
        """
        print('增加.........')
        print(payload)
        if payload['status']:
            # 处理图片及其路径
            location_img_json = payload['receive_data'].pop('location_img_json')
            if location_img_json:
                location_img_path_and_name = payload['receive_data']['location_img_path']
                location_img_path = location_img_path_and_name.rsplit('/', 1)[0] + '/'
                # 判断是否存在路径
                mkdir_path(path=location_img_path)
                location_img_bytes = eval(json.loads(location_img_json.strip('\r\n')))
                print('location_img_path_and_name======', location_img_path_and_name)
                with open(location_img_path_and_name, 'wb') as f:
                    f.write(location_img_bytes)

            gw_ntid = payload['receive_data']['network_id'].rsplit('.', 1)[0] + '.0'
            gateway_obj = models.Gateway.objects.filter(network_id=gw_ntid).first()
            payload['receive_data']['gateway'] = gateway_obj

            if 'delete_status' in list(payload['receive_data'].keys()):  # 判断是软删除，则更新
                models.Sensor.objects.filter(network_id=payload['receive_data']['network_id']).update(
                    **payload['receive_data'])
            else:
                models.Sensor.objects.create(**payload['receive_data'])
        # Log
        views.log.log(payload['status'], payload['msg'], payload['receive_data']['network_id'], payload['user'])

    def remove_sensor(self, payload):
        """
        接收到网关的数据进行删除传感器
        :param payload:
        :return:
        """
        print('删除.........')
        if payload['status']:
            sensor_id = payload['receive_data']['sensor_id']
            if payload['receive_data']['forcedelete']:
                models.Sensor.objects.filter(sensor_id=sensor_id).delete()
            else:
                models.Sensor.objects.filter(sensor_id=sensor_id).update(delete_status=1)
        # Log
        views.log.log(payload['status'], payload['msg'], payload['receive_data']['network_id'], payload['user'])

    def update_gateway(self, payload):
        """
        更新网关
        :param payload:
        :return:
        """
        print('update网关.........')
        if payload['status']:
            gw_network_id = payload['gateway_data']['network_id']
            if models.Gateway.objects.filter(network_id=gw_network_id).exists():
                # 防止网关在未链接服务器的情况下添加网关，连上服务器后可以通过更新网关的操作在服务器端添加网关
                models.Gateway.objects.filter(network_id=gw_network_id).update(**payload['gateway_data'])
            else:
                self.add_gateway(payload)
        # Log
        views.log.log(payload['status'], payload['msg'], payload['gateway_data']['network_id'], payload['user'])
        global update_gw_payload
        update_gw_payload = payload

    def add_gateway(self, payload):
        """
        增加网关，并关联该网关到该公司的每个用户
        :param payload:
        :return:
        """
        print('add网关.........')
        if payload['status']:
            models.Gateway.objects.create(**payload['gateway_data'])
            Enterprise = payload['gateway_data']['Enterprise']
            network_id = payload['gateway_data']['network_id']
            gateway_nid = models.Gateway.objects.filter(network_id=network_id).values('id')[0]['id']
            user_obj_list = models.UserProfile.objects.filter(gateway__Enterprise=Enterprise).all()
            for user_item in user_obj_list:
                user_item.gateway.add(gateway_nid)
        # Log
        views.log.log(payload['status'], payload['msg'], payload['gateway_data']['network_id'], payload['user'])
        global add_gw_payload
        add_gw_payload = payload

    def gwdata(self, payload):
        """
        接收网关获取的传感器的数据
        :param payload:
        :return:
        """
        gwData = payload['gwData']
        print('取数.......')
        sensor_obj = models.Sensor.objects.filter(network_id=payload['network_id'])
        if payload['status']:
            gwData['network_id'] = sensor_obj[0]
            models.Waveforms.objects.create(**gwData)
            # 更新最新电量信息到对应传感器
            sensor_obj.update(battery=gwData['battery'], sensor_online_status=1)
        else:  # 未采集到数据，传感器在线状态变成离线
            sensor_obj.update(sensor_online_status=0)
        global recv_gwdata_payload
        recv_gwdata_payload = payload

    def pause_sensor(self, payload):
        """
        暂停传感器
        :param payload:
        :return:
        """
        print('暂停传感器.......')
        if payload['status']:
            network_id = payload['network_id']
            models.Sensor.objects.filter(network_id=network_id).update(sensor_run_status=0)
        # Log
        views.log.log(payload['status'], payload['msg'], payload['network_id'], payload['user'])
        global pause_payload
        pause_payload = payload

    def resume_sensor(self, payload):
        """
        恢复传感器
        :param payload:
        :return:
        """
        print('恢复传感器.......')
        if payload['status']:
            network_id = payload['network_id']
            models.Sensor.objects.filter(network_id=network_id).update(sensor_run_status=1)
        # Log
        views.log.log(payload['status'], payload['msg'], payload['network_id'], payload['user'])
        global resume_payload
        resume_payload = payload

    def set_sensor_params(self, payload):
        """
        接收传感器增益等参数
        :param payload:
        :return:
        """
        if payload['status']:
            network_id = payload['network_id']
            params_dict = payload['params_dict']
            models.Sensor.objects.filter(network_id=network_id).update(**params_dict)
        # Log
        views.log.log(payload['status'], payload['msg'], payload['network_id'], payload['user'])

    def send_network_id_to_queue(self, payload):
        """
        把接收网关发送过来的要采样的network_id加入队列中，
        如果该公司没有队列，则动态生成该公司的队列对象
        :param payload:
        :return:
        """
        network_id_list = payload['network_id_list']
        Enterprise = payload['Enterprise']
        level = payload['level']
        HZ_Enterprisea_name = lazy_pinyin(Enterprise)
        queue_obj_name = "".join((str(i) for i in HZ_Enterprisea_name))
        if not generate_queue.get(queue_obj_name):
            print('没有，创建。。。')
            generate_queue[queue_obj_name] = PriorityQueue()
            threading.Thread(target=send_to_gw, args=(generate_queue[queue_obj_name],)).start()
        queue_obj = generate_queue.get(queue_obj_name)
        # 把network_id_list中的network_id放到队列
        for network_id in network_id_list:
            queue_obj.put((level, network_id))
        print(queue_obj.queue)


def send_to_gw(queue_obj):
    """
    取出队列命令，发送给网关进行采样
    :param queue_obj: 每个公司的队列对象
    :return:
    """
    while True:
        print(queue_obj.queue)
        network_id = queue_obj.get()[1]
        print('取队列数据。。。', time.time())
        topic = network_id.rsplit('.', 1)[0] + '.0'
        print(network_id)
        send_data = {'id': 'server', 'header': 'get_data', 'data': network_id}
        client.publish(topic, json.dumps(send_data), 2)
        recv_gwdata_start_time = time.time()
        # 接收到网关处理好的结果，用于把操作返回的信息展示到页面
        global recv_gwdata_payload
        recv_gwdata_payload = {}  # 接收之前先清除payload中的缓存数据
        while (time.time() - recv_gwdata_start_time) < 60:
            time.sleep(0.5)
            if recv_gwdata_payload:
                break
        if not recv_gwdata_payload:
            # 超时时间到，未返回任何数据，则显示采样失败信息，网关未响应
            send_data = {'id': 'client', 'header': 'gwdata', 'status': False, 'msg': '[%s]获取失败，网关未响应。' % network_id}
            client.publish(topic, json.dumps(send_data), 2)
            # Log
            views.log.log(send_data['status'], send_data['msg'], network_id)
        else:
            # Log
            views.log.log(recv_gwdata_payload['status'], recv_gwdata_payload['msg'], network_id)


class HandleImgs(object):
    """处理图片"""

    def __init__(self):
        pass

    def get_size(self, file):
        """获取文件大小：KB"""
        size = os.path.getsize(file)
        return size / 1024

    def get_outfile(self, infile, outfile):
        """拼接输出文件地址"""
        if outfile:
            return outfile
        dir, suffix = os.path.splitext(infile)
        outfile = '{}-out{}'.format(dir, suffix)
        return outfile

    def compress_image(self, infile, outfile='', mb=100, step=10, quality=80):
        """不改变图片尺寸压缩到指定大小
        :param infile: 压缩源文件
        :param outfile: 压缩文件保存地址
        :param mb: 压缩目标，KB
        :param step: 每次调整的压缩比率
        :param quality: 初始压缩比率
        :return: 压缩文件地址，压缩文件大小
        """
        o_size = self.get_size(infile)
        if o_size <= mb:
            return infile
        outfile = self.get_outfile(infile, outfile)
        while o_size > mb:
            im = Image.open(infile)
            im.save(outfile, quality=quality)
            if quality - step < 0:
                break
            quality -= step
            o_size = self.get_size(outfile)
        # 删除原文件，修改新文件名称
        old_file_name = infile
        os.remove(infile)
        os.rename(outfile, old_file_name)

    def resize_image(self, infile, outfile='', x_s=400):
        """修改图片尺寸
        :param infile: 图片源文件
        :param outfile: 重设尺寸文件保存地址
        :param x_s: 设置的宽度
        :return:
        """
        im = Image.open(infile)
        x, y = im.size
        y_s = int(y * x_s / x)
        out = im.resize((x_s, y_s), Image.ANTIALIAS)
        outfile = self.get_outfile(infile, outfile)
        out.save(outfile)
        # 删除原文件，修改新文件名称
        old_file_name = infile
        os.remove(infile)
        os.rename(outfile, old_file_name)


def handle_img_and_data(request):
    """
    压缩剪裁图片，合并数据格式
    :param request:
    :return:
    """
    handleimgs = HandleImgs()
    data = json.loads(request.POST.get('data'))
    exist_img_path = data.pop('exist_img_path')
    location_img_obj = request.FILES.get('location_img_obj')
    # 判断是否有路径，没有就创建
    gw_network_id = data['network_id'].rsplit('.', 1)[0] + '.0'
    print('gw_network_id', gw_network_id)
    Base_img_path = mkdir_path(gw_network_id=gw_network_id)
    print('Base_img_path', Base_img_path)
    if location_img_obj:
        img_name = location_img_obj.name
        # 写图片
        with open(Base_img_path + location_img_obj.name, 'wb') as f:
            f.write(location_img_obj.read())
        # 压缩图片
        handleimgs.compress_image(Base_img_path + location_img_obj.name)
        # 裁剪图片
        handleimgs.resize_image(Base_img_path + location_img_obj.name)
        # 处理数据格式
        with open(Base_img_path + location_img_obj.name, 'rb') as ff:
            img_bytes = ff.read()
        img_json = json.dumps(str(img_bytes))
        data['location_img_json'] = img_json
        data['location_img_path'] = Base_img_path + img_name
    else:
        data['location_img_json'] = ''
        if exist_img_path:
            data['location_img_path'] = Base_img_path + exist_img_path.rsplit('/', 1)[1]
        else:
            data['location_img_path'] = ''
    return data


def mkdir_path(path=None, gw_network_id=None):
    """
    判断是否有路径，没有则创建
    :param path:
    :param gw_network_id:
    :return:
    """
    if path:  # gw发送过来的path
        if not os.path.exists(path):
            os.mkdir(path)
    elif gw_network_id:  # server前端传过来的gw_network_id
        path = 'static/location_imgs_%s/' % gw_network_id
        if not os.path.exists(path):
            os.mkdir(path)
    return path


def corrosion_rate(network_id):
    """
    计算腐蚀率
    :param data_latest:
    :param data_first:
    :return:
    """
    data_list = list(models.Waveforms.objects.filter(network_id=network_id).values('time_tamp', 'thickness'))

    data_list = [item for item in data_list if item['thickness'] != 0.0]

    if data_list:
        first_time_tamp = datetime.strptime(data_list[0]['time_tamp'], "%Y-%m-%d %H:%M:%S").timestamp()
        latest_struct_time = data_list[-1:][0]['time_tamp']
        if int(timestamp(latest_struct_time, first_time_tamp)) > 14:  # 如果采集数据的天数不少于15天，则可以计算腐蚀率
            y = np.array([item['thickness'] for item in data_list])
            x = np.array([timestamp(item['time_tamp'], first_time_tamp) for item in data_list])
            corrosion_rate = skl_func(x, y)
            # plt.legend(loc="upper left")
            # plt.show()
            corrosion_rate = round(float(abs(corrosion_rate * 365)), 3)
        else:
            corrosion_rate = '需要更多数据！'
    else:
        corrosion_rate = '需要更多数据！'

    return corrosion_rate


def skl_func(x, y):
    """
    最小二分法计算斜率
    :param x:
    :param y:
    :return:
    """
    lr = LinearRegression()
    lr.fit(x.reshape(-1, 1), y)
    # y_hat = lr.predict(np.arange(0, 10, 0.75).reshape(-1, 1))
    # print('skl_func:\tW = %f\n\tb = %f' % (lr.coef_, lr.intercept_))
    # plt.scatter(x, y)
    # plt.plot(np.arange(0, 10, 0.75), y_hat, color='g', marker='x', label='skl_func')
    return lr.coef_


def timestamp(struct_time, first_time_tamp):
    """
    结构化时间转成时间戳，计算与第一天的间隔时间，单位为天
    :param struct_time:
    :return:
    """
    time_stamp = datetime.strptime(struct_time, "%Y-%m-%d %H:%M:%S").timestamp()
    x = (time_stamp - first_time_tamp) / (3600 * 24)
    return x


def cal_thickness_avg(data_list):
    """
    计算厚度平均值，*2后用于设置chart的y轴上限
    :param data_list:
    :return:
    """
    data_list = [item for item in data_list if item['thickness'] != 0.0]
    thickness_total = 0
    thickness_num = len(data_list)
    for item in data_list:
        thickness_total += item['thickness']
    thickness_avg = thickness_total / thickness_num

    return thickness_avg


def cal_alarm_val(sensor_item):
    """
    计算报警值
    :param sensor_item:
    :return:
    """
    alarm_sensor_list = []
    alias = sensor_item['alias']
    network_id = sensor_item['network_id']
    alarm_thickness = sensor_item['alarm_thickness'] if sensor_item['alarm_thickness'] else 0
    alarm_battery = sensor_item['alarm_battery'] if sensor_item['alarm_battery'] else 0
    alarm_temperature = sensor_item['alarm_temperature'] if sensor_item['alarm_temperature'] else 350
    alarm_corrosion = sensor_item['alarm_corrosion'] if sensor_item['alarm_corrosion'] else 50
    latest_vals = models.Waveforms.objects.values('thickness', 'temperature', 'battery', 'time_tamp').filter(network_id=sensor_item['network_id'])
    latest_corrosion = corrosion_rate(network_id)

    if latest_vals:
        if not sensor_item['sensor_online_status']:
            alarm_sensor_list.append(
                {alias: {'报警信息：': '传感器离线！',
                         '报警信息1：': '/',
                         '报警信息2：': '/',
                          '报警时间：': '/',
                         'network_id': network_id}})
        if latest_vals.last()['thickness'] < alarm_thickness:
            alarm_sensor_list.append(
                {alias: {'报警信息：': '厚度报警！（mm）',
                         '报警厚度（mm）：': alarm_thickness,
                         '当前厚度（mm）：': latest_vals.last()['thickness'],
                          '报警时间：': latest_vals.last()['time_tamp'],
                         'network_id': network_id}})
        if latest_vals.last()['battery'] < alarm_battery:
            alarm_sensor_list.append(
                {alias: {'报警信息：': '电量报警！（%）',
                         '报警电量（%）：': alarm_battery,
                         '当前电量（%）：': latest_vals.last()['battery'],
                         '报警时间：': latest_vals.last()['time_tamp'],
                         'network_id': network_id}})
        if latest_vals.last()['temperature'] > alarm_temperature:
            alarm_sensor_list.append(
                {alias: {'报警信息：': '温度报警！（℃）',
                         '报警温度（℃）：': alarm_temperature,
                         '当前温度（℃）：': latest_vals.last()['temperature'],
                         '报警时间：': latest_vals.last()['time_tamp'],
                         'network_id': network_id}})
        if latest_corrosion != '需要更多数据！' and latest_corrosion > alarm_corrosion:
            alarm_sensor_list.append(
                {alias: {'报警信息：': '腐蚀率报警！（mm/年）',
                         '报警腐蚀率（mm/年）：': alarm_corrosion,
                         '当前腐蚀率（mm/年）：': latest_corrosion,
                         '报警时间：': latest_vals.last()['time_tamp'],
                         'network_id': network_id}})

    return alarm_sensor_list


def judge_user_id(request, nid):
    """
    如果不是超级管理员，则需要判断进入的编辑用户页面是否是自己公司的员工id，防止手动输入参数为其他公司员工id的url
    :param request:
    :param nid:
    :return:
    """
    user_id_conform = True
    cur_user_obj = models.UserProfile.objects.filter(id=request.user.id)
    cur_role = cur_user_obj[0].role.values('name').all()
    role_list = [item['name'] for item in cur_role]
    if 'super_root' not in role_list and 'create_root' not in role_list:
        cur_user_enterprise = cur_user_obj[0].gateway.values('Enterprise')[0]['Enterprise']
        cur_enterprise_user_list = models.UserProfile.objects.filter(gateway__Enterprise=cur_user_enterprise).values('id')
        cur_enterprise_user_id_list = [item['id'] for item in cur_enterprise_user_list]
        if nid not in cur_enterprise_user_id_list:
            user_id_conform = False

    return user_id_conform


def show_selected_permissions(request, Group, nid):
    """
    在编辑用户页面显示选中的用户权限
    :return:
    """
    # 当前登录用户所拥有的角色权限和被手动分配的权限
    cur_user_role_permissions_list = list(
        Group.objects.values('permissions__id', 'permissions__name').filter(user=request.user.id))
    cur_user_manual_assign_permissions_list = models.UserProfile.objects.get(
        id=request.user.id).user_permissions.values('id', 'name').all()
    # 当前被选中要修改的用户所拥有的角色权限和被手动分配的权限
    selected_user_role_permissions_list = list(Group.objects.values('permissions__id').filter(user=nid))
    print('selected_user_role_permissions_list', selected_user_role_permissions_list)
    selected_user_manual_assign_permissions_list = models.UserProfile.objects.get(id=nid).user_permissions.values(
        'id').all()
    # 变换key保持一致
    cur_user_all_permissions_list = []
    for item in cur_user_manual_assign_permissions_list:
        item_temp = {}
        item_temp['permissions__id'] = item['id']
        item_temp['permissions__name'] = item['name']
        cur_user_all_permissions_list.append(item_temp)
    # 当前登录用户所拥有的角色权限和被手动分配的权限的总和
    cur_user_all_permissions_list += cur_user_role_permissions_list
    cur_user_all_permissions_list = list_dict_duplicate_removal(cur_user_all_permissions_list)
    # 当前被选中要修改的用户所拥有的角色权限和被手动分配的权限的总和
    selected_user_permissions_list = [item['permissions__id'] for item in selected_user_role_permissions_list] + \
                                     [item['id'] for item in selected_user_manual_assign_permissions_list]
    selected_user_permissions_list = list_dict_duplicate_removal(selected_user_permissions_list)
    return cur_user_all_permissions_list, selected_user_permissions_list


def list_dict_duplicate_removal(distinct_list):
    """
    给列表中的字典去重
    :param distinct_list:
    :return:
    """
    run_function = lambda x, y: x if y in x else x + [y]
    return reduce(run_function, [[], ] + distinct_list)


#######################################################
handle_func_obj = HandleFunc()


def handle_recv_gwdata(payload):
    """
    处理接收到的网关数据
    :param payload:
    :return:
    """
    header = payload['header']
    # 反射
    getattr(handle_func_obj, header)(payload)
#######################################################

