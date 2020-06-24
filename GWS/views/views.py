from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from GWS import models
from GWS import permissions
from apscheduler.schedulers.background import BackgroundScheduler
from GatewayServer import settings
import json, time
from utils.check_click_method import check_click_method
# from utils.mqtt_client import MQTT_Client
from utils.mqtt_client import client
from lib.log import Logger
from utils import handle_func


heart_sche = BackgroundScheduler()
log = Logger()


@login_required
def index(request):
    """
    首页
    :param request:
    :return:
    """
    gwntid_list = []
    all_sensor_count = 0
    user_obj = models.UserProfile.objects.filter(name=request.user).first()
    gateway_obj = user_obj.gateway.all()
    gw_status = {'在线': 1, '离线': 0}
    for gw_item in gateway_obj:
        sensor_count = models.Sensor.objects.filter(gateway=gw_item, delete_status=0).count()
        all_sensor_count += sensor_count

    all_sensor_list = []
    all_alarm_sensor_list = []
    for gateway_item in gateway_obj.values('network_id', 'name'):
        gw_network_id = gateway_item['network_id']
        gwntid_list.append(gw_network_id)
        gw_name = gateway_item['name']
        sensor_obj_list = list(models.Sensor.objects.filter(gateway__network_id=gw_network_id, delete_status=0).\
            values('network_id', 'alias', 'gateway__name', 'sensor_run_status', 'sensor_online_status',
                   'alarm_thickness', 'alarm_battery', 'alarm_temperature', 'alarm_corrosion', 'longitude', 'latitude'))
        sensor_run_status = {'开通': 1, '禁止': 0}
        sensor_online_status = {'在线': 1, '离线': 0}
        for sensor_item in sensor_obj_list:
            alarm_sensor_list = handle_func.cal_alarm_val(sensor_item)
            all_alarm_sensor_list += alarm_sensor_list
        all_alarm_sensor_count = len(all_alarm_sensor_list)
        all_sensor_list += sensor_obj_list
    all_sensor_list_json = json.dumps(all_sensor_list)
    # 把gwntid写进session,以便websocket使用
    request.session['gwntid_list'] = gwntid_list

    return render(request, 'index.html', locals())


@csrf_exempt
@permissions.check_permission
@login_required
def manual_config(request):
    """
    手动调试
    :param request:
    :return:
    """
    if request.method == 'GET':
        last_time_gwntid = request.session.get('gwntid_and_snrntid', {'gw': '', 'snr': ''})['gw']
        last_time_snrntid = request.session.get('gwntid_and_snrntid', {'gw': '', 'snr': ''})['snr']
        user_obj = models.UserProfile.objects.filter(name=request.user).first()
        gateway_obj = user_obj.gateway.all().values('name', 'network_id')

        latest_data = []
        for gateway_item in gateway_obj:
            gw_network_id = gateway_item['network_id']
            single_gateway_latest_data = list(models.Waveforms.objects.values('id',
                                                          'network_id__alias',
                                                          'time_tamp',
                                                          'thickness',
                                                          'temperature',
                                                          'gain',
                                                          'battery').filter(
                network_id__gateway__network_id=gw_network_id).order_by('-id'))[:5]
            latest_data += single_gateway_latest_data
        latest_data.sort(key=lambda data: data['id'], reverse=True)

    if request.method == 'POST':
        payload = {}
        response = {'status': False, 'msg': "加入队列失败"}
        sensor_network_id = request.POST.get('sensor_network_id')
        gateway_network_id = request.POST.get('gateway_network_id')
        # 把sensor_network_id和gateway_network_id存到session中，刷新页面可保存上次操作内容
        request.session['gwntid_and_snrntid'] = {'gw': gateway_network_id, 'snr': sensor_network_id}
        try:
            if sensor_network_id != '':
                gateway_network_id = sensor_network_id.rsplit('.', 1)[0] + '.0'
                Enterprise = models.Gateway.objects.values('Enterprise').get(network_id=gateway_network_id)['Enterprise']
                payload['network_id_list'] = [sensor_network_id]
                payload['Enterprise'] = Enterprise
                payload['level'] = 1
                # 加入队列
                handle_func.handle_func_obj.send_network_id_to_queue(payload)
                response = {'status': True, 'msg': "成功加入采样队列，请稍等..."}
        except KeyError:
            print('没有这个传感器')

        return HttpResponse(json.dumps(response))

    return render(request, 'GWS/manual_config.html', locals())


@permissions.check_permission
@login_required
def sensor_manage(request):
    """
    传感器管理
    :param request:
    :return:
    """
    if request.method == 'GET':
        user_obj = models.UserProfile.objects.filter(name=request.user).first()
        gateway_obj = user_obj.gateway.all().values('network_id', 'name')
        all_sensor_list = []
        last_sample_time_list = []
        for gateway_item in gateway_obj:
            gw_network_id = gateway_item['network_id']
            gw_name = gateway_item['name']
            sensor_obj_list = models.Sensor.objects.filter(gateway__network_id=gw_network_id)
            for sensor_item in sensor_obj_list:
                sensor_type = {'ETM-100': 0}
                Importance = {'一般': 0, '重要': 1}
                material = models.Material.objects.values('id', 'name').all().order_by('id')
                sensor_run_status = {'开通': 1, '禁止': 0}
                sensor_online_status = {'在线': 1, '离线': 0}
                last_sample_time = sensor_item.waveforms_set.values('network_id', 'time_tamp').last()
                if last_sample_time:
                    last_sample_time_list.append(last_sample_time)
            sensor_list = sensor_obj_list.values('sensor_id', 'network_id', 'received_time_data', 'alias', 'battery',
                                                 'location', 'date_of_installation', 'gateway__name', 'area', 'material',
                                                 'sensor_run_status', 'sensor_online_status', 'sensor_type',
                                                 'Importance', 'delete_status', 'description')
            all_sensor_list += sensor_list

    return render(request, 'GWS/sensor_manage.html', locals())


@permissions.check_permission
@login_required
def gateway_manage(request):
    """
    网关管理
    :param request:
    :return:
    """
    if request.method == 'GET':
        user_obj = models.UserProfile.objects.filter(name=request.user).first()
        gateway_obj = user_obj.gateway.all()
        print(gateway_obj)
        gw_status = {'在线': 1, '离线': 0}

    return render(request, 'GWS/gateway_manage.html', locals())


@login_required
# @permissions.check_permission
def edit_sensor_params(request):
    """
    传感器参数详情
    :param request:
    :return:
    """
    context = {
        "cHz": [cHz for cHz in range(1, 4)],
        "gain": [gain for gain in range(60, 101)],
        "avg_time": [avg_time for avg_time in range(0, 11)],
        "Hz": [Hz for Hz in range(2, 5)],
        "Sample_depth": [Sample_depth for Sample_depth in range(0, 3)],
        "Sample_Hz": [200, 5000],
    }
    user_obj = models.UserProfile.objects.filter(name=request.user).first()
    gateway_obj = user_obj.gateway.all().values('network_id', 'name')
    all_sensor_list = []
    last_sample_time_list = []
    for gateway_item in gateway_obj:
        gw_network_id = gateway_item['network_id']
        gw_name = gateway_item['name']
        sensor_list = models.Sensor.objects.filter(gateway__network_id=gw_network_id, delete_status=0)
        all_sensor_list += sensor_list

    return render(request, "GWS/edit_sensor_params.html", locals())


@login_required
def all_data_report(request):
    """
    全部数据
    :param request:
    :return:
    """
    user_obj = models.UserProfile.objects.filter(name=request.user).first()
    gateway_obj = user_obj.gateway.all().values('network_id')
    all_sensor_list = []
    all_data_obj_list = []
    for gateway_item in gateway_obj:
        gw_network_id = gateway_item['network_id']
        sensor_obj_list = models.Sensor.objects.filter(gateway__network_id=gw_network_id)
        all_sensor_list += sensor_obj_list
    for sensor_item in all_sensor_list:
        data_obj = list(models.Waveforms.objects.values('id', 'network_id', 'network_id__alias', 'time_tamp',
                                               'battery', 'temperature', 'thickness').filter(network_id=sensor_item).order_by('-id'))
        all_data_obj_list += data_obj
    return render(request, 'GWS/all_data_report.html', locals())


@login_required
def thickness_report(request):
    """
    单个传感器厚度曲线
    :param request:
    :return:
    """
    data_obj = models.Waveforms.objects.values('network_id', 'network_id__alias').distinct()
    print(data_obj)
    user_obj = models.UserProfile.objects.filter(name=request.user).first()
    gateway_obj = user_obj.gateway.all().values('name', 'network_id')
    return render(request, 'GWS/thickness_report.html', locals())


@login_required
def corrosion_rate_list(request):
    """
    腐蚀速率列表
    :param request:
    :return:
    """
    user_obj = models.UserProfile.objects.filter(name=request.user).first()
    gateway_obj = user_obj.gateway.all().values('network_id', 'name')
    all_sensor_list = []
    for gateway_item in gateway_obj:
        gw_network_id = gateway_item['network_id']
        gw_name = gateway_item['name']
        sensor_obj_list = models.Sensor.objects.filter(gateway__network_id=gw_network_id, delete_status=0)
        for sensor_item in sensor_obj_list:
            material = models.Material.objects.values('id', 'name').all().order_by('id')
        sensor_list = list(sensor_obj_list.values('sensor_id', 'network_id', 'alias', 'gateway__name', 'material'))
        print(sensor_list)
        for item in sensor_list:
            network_id = item['network_id']
            # 计算腐蚀速率
            corrosion_rate = handle_func.corrosion_rate(network_id)
            item['corrosion_rate'] = corrosion_rate

        all_sensor_list += sensor_list
    return render(request, 'GWS/corrosion_rate.html', locals())


@permissions.check_permission
@login_required
@check_click_method
def add_sensor(request, network_id):
    """
    增加传感器页面
    :param request:
    :return:
    """
    user_obj = models.UserProfile.objects.filter(name=request.user).first()
    gateway_obj = user_obj.gateway.all().values('name', 'network_id')
    sensor_obj = models.Sensor.objects.first()
    sensor_type = {'ETM-100': 0}
    Importance = {'一般': 0, '重要': 1}
    material = models.Material.objects.values('id', 'name').all().order_by('id')
    longitude = 0.0
    latitude = 0.0
    context = {
        "month_cron": [i for i in range(1, 13)],
        "day_cron": [i for i in range(1, 29)],
        "hour_cron": [i for i in range(0, 24)],
        "minute_cron": [i for i in range(0, 60)],
    }
    return render(request, 'GWS/add_sensor.html', locals())


@login_required
@csrf_exempt
def alarm_sensor_list(request):
    """
    报警传感器信息
    :param request:
    :return:
    """
    if request.method == 'POST':
        all_alarm_sensor_list = eval(request.POST.get('all_alarm_sensor_list'))

        return render(request, 'GWS/alarm_sensor_list.html', locals())\


@login_required
@csrf_exempt
def export_data(request):
    """
    导出数据
    :param request:
    :return:
    """

    return render(request, 'GWS/export_data.html', locals())


@login_required
@check_click_method
def sensor_data_info(request, network_id):
    """
    传感器数据详情
    :param request:
    :return:
    """
    sensor_obj = models.Sensor.objects.filter(network_id=network_id).first()
    gateway_name = models.Sensor.objects.values('gateway__name').filter(network_id=network_id)[0]['gateway__name']
    material_id = models.Sensor.objects.values('material').filter(network_id=network_id)[0]['material']
    material = models.Material.objects.values('name').get(id=material_id)['name']
    sensor_type = sensor_obj._meta.get_field("sensor_type")
    Importance = sensor_obj._meta.get_field("Importance")
    sensor_run_status = sensor_obj._meta.get_field("sensor_run_status")
    sensor_online_status = sensor_obj._meta.get_field("sensor_online_status")
    last_data_obj = models.Waveforms.objects.values('thickness', 'battery', 'time_tamp', 'temperature').\
        filter(network_id_id=network_id).last()
    data_count = models.Waveforms.objects.filter(network_id_id=network_id).count()
    received_time_data = eval(
        models.Sensor.objects.filter(network_id=network_id).values('received_time_data')[0]['received_time_data'])
    if last_data_obj:
        now_thickness = last_data_obj['thickness']
        battery = last_data_obj['battery']
        temperature = last_data_obj['temperature']
        time_tamp = last_data_obj['time_tamp']
    else:
        now_thickness = '暂无数据'
        battery = '暂无数据'
    return render(request, 'GWS/sensor_data_info.html', locals())


@permissions.check_permission
@login_required
@check_click_method
def edit_sensor(request, sensor_id):
    """
    编辑传感器信息
    :param request:
    :param sensor_id:
    :return:
    """
    received_time_data = eval(
        models.Sensor.objects.filter(sensor_id=sensor_id).values('received_time_data')[0]['received_time_data'])
    sensor_obj = models.Sensor.objects.get(sensor_id=sensor_id)
    date_of_installation = str(sensor_obj.date_of_installation)
    # sensor_type = sensor_obj._meta.get_field('sensor_type')
    # Importance = sensor_obj._meta.get_field('Importance')
    sensor_type = {'ETM-100': 0}
    Importance = {'一般': 0, '重要': 1}
    material = models.Material.objects.values('id', 'name').all().order_by('id')
    context = {
        "month_cron": [i for i in range(1, 13)],
        "day_cron": [i for i in range(1, 29)],
        "hour_cron": [i for i in range(0, 24)],
        "minute_cron": [i for i in range(0, 60)],
    }

    return render(request, 'GWS/edit_sensor.html', locals())


@permissions.check_permission
@login_required
@check_click_method
def edit_sensor_alarm_msg(request, sensor_id):
    """
    编辑传感器报警信息
    :param request:
    :param sensor_id:
    :return:
    """
    sensor_obj = models.Sensor.objects.get(sensor_id=sensor_id)

    return render(request, 'GWS/edit_sensor_alarm_msg.html', locals())


@permissions.check_permission
@login_required
@check_click_method
def edit_gateway(request, network_id):
    """
    编辑网关信息
    :param request:
    :param network_id:
    :return:
    """
    gateway_obj = models.Gateway.objects.filter(network_id=network_id).values('name', 'Enterprise', 'gw_status', 'network_id')[0]
    print(gateway_obj)
    gw_status = {'在线': 1, '离线': 0}

    return render(request, 'GWS/set_gateway.html', locals())


@permissions.check_permission
@login_required
@check_click_method
def resume_sensor(request, sensor_id):
    """
    开通/恢复传感
    :param request:
    :param sensor_id:
    :return:
    """
    response = {'status': False, 'msg': '开通失败'}
    network_id = models.Sensor.objects.filter(sensor_id=sensor_id).values('network_id')[0]['network_id']
    gateway_network_id = network_id.rsplit('.', 1)[0] + '.0'
    send_data = {'id': 'server', 'header': 'resume_sensor', 'network_id': network_id, 'user': str(request.user)}
    print('send_data', send_data)
    client.publish(gateway_network_id, json.dumps(send_data), 2)
    resume_start_time = time.time()
    # 接收到网关处理好的结果，用于把操作返回的信息展示到页面
    while (time.time() - resume_start_time) < 3:
        if handle_func.resume_payload:
            msg = handle_func.resume_payload['msg']
            status = handle_func.resume_payload['status']
            response = {'status': status, 'msg': msg}
            break
    handle_func.resume_payload = {}

    return render(request, 'GWS/resume_sensor.html', locals())


@permissions.check_permission
@login_required
@check_click_method
def pause_sensor(request, sensor_id):
    """
    禁止/暂停传感器
    :param request:
    :param sensor_id:
    :return:
    """
    response = {'status': False, 'msg': '禁用失败'}
    network_id = models.Sensor.objects.filter(sensor_id=sensor_id).values('network_id')[0]['network_id']
    gateway_network_id = network_id.rsplit('.', 1)[0] + '.0'
    send_data = {'id': 'server', 'header': 'pause_sensor', 'network_id': network_id, 'user': str(request.user)}
    print('send_data', send_data)
    print('gateway_network_id', gateway_network_id)
    client.publish(gateway_network_id, json.dumps(send_data), 2)
    remove_start_time = time.time()
    # 接收到网关处理好的结果，用于把操作返回的信息展示到页面
    while (time.time() - remove_start_time) < 3:
        if handle_func.pause_payload:
            msg = handle_func.pause_payload['msg']
            status = handle_func.pause_payload['status']
            response = {'status': status, 'msg': msg}
            break
    handle_func.pause_payload = {}

    return render(request, 'GWS/pause_sensor.html', locals())


@csrf_exempt
@permissions.check_permission
@login_required
def send_server_data(request):
    """
    发送数据到网关
    :param request:
    :return:
    """
    response = {'status': False, 'msg': '网关未响应'}
    if request.method == 'POST':

        server_data = handle_func.handle_img_and_data(request)

        sensor_network_id = server_data['network_id']
        received_time_data = server_data.get('received_time_data')
        print("received_time_data", received_time_data)

        gateway_network_id = sensor_network_id.rsplit('.', 1)[0] + '.0'

        if server_data['choice'] == 'update':
            print('更新.....')
            send_data = {'id': 'server', 'header': 'update_sensor', 'data': server_data, 'user': str(request.user)}
            print('send_data', send_data)
            client.publish(gateway_network_id, json.dumps(send_data), 2)

        elif server_data['choice'] == 'add':
            print('增加.....')
            send_data = {'id': 'server', 'header': 'add_sensor', 'data': server_data, 'user': str(request.user)}
            print('send_data', send_data)
            client.publish(gateway_network_id, json.dumps(send_data), 2)

        elif server_data['choice'] == 'remove':
            print('删除.....')
            send_data = {'id': 'server', 'header': 'remove_sensor', 'data': server_data, 'user': str(request.user)}
            print('send_data', send_data)
            client.publish(gateway_network_id, json.dumps(send_data), 2)

    return HttpResponse(json.dumps(response))


@login_required
def thickness_json_report(request):
    """
    从数据库中获取厚度值进行绘图
    :param request:
    :return:
    """
    network_id = request.GET.get('network_id')
    response = {'datas': [{'name': '厚度值', 'data': []}]}
    try:
        alias = models.Sensor.objects.filter(network_id=network_id).values('alias')[0]['alias']
        data_obj = list(models.Waveforms.objects.filter(network_id=network_id).values('id', 'time_tamp', 'thickness'))
        thickness_avg = handle_func.cal_thickness_avg(data_obj)
        data_list = []
        for item in data_obj:
            data_temp = {}
            data_temp['y'] = float(item.pop('thickness'))
            data_temp['name'] = str(item.pop('id')) + ":" + item.pop('time_tamp')
            data_list.append(data_temp)
        response['datas'] = [{'name': '厚度值', 'data': data_list}]
        response['alias'] = alias
        response['yAxis_max_limit'] = thickness_avg * 2
    except Exception as e:
        print(e)

    return HttpResponse(json.dumps(response))


@login_required
def corrosion_rate_json_report(request):
    """
    计算腐蚀速率
    :param request:
    :return:
    """
    network_id = request.GET.get('network_id')
    corrosion_rate = 0
    try:
        # 计算腐蚀速率
        corrosion_rate = handle_func.corrosion_rate(network_id)

    except Exception as e:
        print(e)

    return HttpResponse(json.dumps(corrosion_rate))


@login_required
@csrf_exempt
def judge_username_exist_json(request):
    """
    判断是否存在用户名
    :param request:
    :return:
    """
    response = {'status': False, 'msg': None}
    name = request.POST.get('name')
    previous_name = request.POST.get('previous_name')
    try:
        if name == previous_name:  # 判断是否修改了用户名
            user_is_exist = None
        else:
            user_is_exist = models.UserProfile.objects.get(name=name)
    except Exception as e:
        user_is_exist = None
    if user_is_exist:
        response = {'status': True, 'msg': '此用户名已存在！'}

    return HttpResponse(json.dumps(response))


@login_required
@csrf_exempt
@check_click_method
def data_json_report(request, nid):
    """
    从数据库中获取数据绘制数据波形图
    :param request:
    :param nid: 网关数据id
    :return:
    """
    response = []
    try:
        data_dict = models.Waveforms.objects.filter(id=nid).values('network_id__sensor_id', 'network_id__alias', 'data', 'time_tamp', 'thickness').first()
        data_list = list(enumerate(eval(data_dict['data'])))
        # print(data_list)
        temp = {
            'name': "--名称：" + data_dict['network_id__alias'] + " --时间：" + data_dict['time_tamp'] + ' --厚度：' + str(data_dict['thickness']),
            'data': data_list
        }
        response.append(temp)
    except Exception as e:
        print(e)

    return HttpResponse(json.dumps(response))


@csrf_exempt
@permissions.check_permission
@login_required
def set_gateway_json(request):
    """
    更新设置网关
    :param request:
    :return:
    """
    response = {'status': False, 'msg': '网关未响应'}
    gateway_data = json.loads(request.POST.get('gateway_data'))
    gateway_obj = models.Gateway.objects.first()
    # print('gateway_data', gateway_data)  # {'Enterprise': '中石油', 'name': '中石油1号网关', 'network_id': '0.0.1.0', 'gw_status': '1'}
    if gateway_obj:
        send_data = {'id': 'server', 'header': 'update_gateway', 'gateway_data': gateway_data, 'user': str(request.user)}
        topic = gateway_data['network_id']
        client.publish(topic, json.dumps(send_data), 2)
        update_gw_start_time = time.time()
        # 接收到网关处理好的结果，用于把操作返回的信息展示到页面
        while (time.time() - update_gw_start_time) < 3:
            if handle_func.update_gw_payload:
                msg = handle_func.update_gw_payload['msg']
                status = handle_func.update_gw_payload['status']
                response = {'status': status, 'msg': msg}
                break
        handle_func.update_gw_payload = {}

    return HttpResponse(json.dumps(response))


@csrf_exempt
@login_required
# @permissions.check_permission
def set_sensor_params(request):
    """
    设置模态框中的传感器参数
    :param request:
    :return:
    """
    result = {'status': False, 'msg': '设置参数失败'}
    val_dict = json.loads(request.POST.get('val_dict'))
    network_id = val_dict.pop('network_id')
    print('val_dict', val_dict)
    try:
        # 判断Sample_Hz参数是否合法
        if int(val_dict['Sample_Hz']) < 200 or int(val_dict['Sample_Hz']) > 5000:
            result = {'status': False, 'msg': '采样频率参数范围：200-5000'}
            return HttpResponse(json.dumps(result))

    except Exception as e:
        print(e, '设置参数失败')
    send_data = {'id': 'server', 'header': 'set_sensor_params', 'val_dict': val_dict, 'network_id': network_id, 'user': str(request.user)}
    topic = network_id.rsplit('.', 1)[0] + '.0'
    client.publish(topic, json.dumps(send_data), 2)

    log.log(result['status'], result['msg'], network_id, str(request.user))

    return HttpResponse(json.dumps(result))


@csrf_exempt
@login_required
def gateway_associated_sensors_json(request):
    """
    查找选择的网关关联的传感器
    :param request:
    :return:
    """
    response = {'status': False, 'msg': ''}
    try:
        gateway_network_id = request.POST.get('gateway_network_id')
        manual_get_bit = request.POST.get('manual_get_bit')
        if manual_get_bit:  # 如果是手动获取，需要排除已经软删除传感器
            sensor_list = list(models.Sensor.objects.values('network_id', 'alias').filter(
                gateway__network_id=gateway_network_id,
                delete_status=0))
        else:
            sensor_list = list(models.Sensor.objects.values('network_id', 'alias').filter(
                gateway__network_id=gateway_network_id))
        response = {'status': True, 'msg': sensor_list}
    except Exception as e:
        print(e)

    return HttpResponse(json.dumps(response))\


@csrf_exempt
@login_required
def show_soundV_json(request):
    """
    查找显示声速
    :param request:
    :return:
    """
    if request.method == 'POST':
        selected_material_id = json.loads(request.POST.get('selected_material_id'))
        soundV = models.Material.objects.values('sound_V').get(id=selected_material_id)['sound_V']
        result = {'soundV': soundV}

        return HttpResponse(json.dumps(result))


def heart_ping():
    """
    ping心跳
    :return:
    """
    result = {'status': True}
    topic = 'pub'
    send_data = {'id': 'server', 'header': 'heart_ping', 'result': result}
    client.publish(topic, json.dumps(send_data), 2)
    models.Gateway.objects.all().update(gw_status=0)


# 每分钟执行一次心跳
try:
    heart_sche.add_job(heart_ping, 'interval', minutes=settings.heart_time['minutes'],
                       seconds=settings.heart_time['seconds'], id="heart_ping")
    heart_sche.start()
except Exception as e:
    print(e)
    heart_sche.shutdown()


def test(request):

    return render(request, 'test.html')




