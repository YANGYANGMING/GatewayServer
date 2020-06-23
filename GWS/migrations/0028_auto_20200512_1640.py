# Generated by Django 2.2.2 on 2020-05-12 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GWS', '0027_auto_20200511_1648'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'permissions': (('GWS_manual_config_view', '可以访问配置时间页面'), ('GWS_manual_config_get_data_view', '可以手动获取数据'), ('GWS_sensor_manage_view', '可以访问传感器管理页面'), ('GWS_gateway_manage_view', '可以访问网关管理页面'), ('GWS_add_sensor_view', '可以访问增加传感器页面'), ('GWS_edit_sensor_view', '可以访问编辑传感器页面'), ('GWS_edit_sensor_alarm_msg_view', '可以访问编辑传感器报警信息页面'), ('GWS_edit_gateway_view', '可以访问编辑网关页面'), ('GWS_resume_sensor_view', '可以开通传感器'), ('GWS_pause_sensor_view', '可以禁用传感器'), ('GWS_send_server_data_view', '可以对传感器进行增删改操作'), ('GWS_set_gateway_json_view', '可以更新网关'), ('GWS_user_add_view', '可以访问增加用户页面'), ('GWS_user_add_save', '可以保存增加的用户信息'), ('GWS_user_edit_view', '可以访问编辑用户页面'), ('GWS_user_edit_save', '可以保存编辑的用户信息'), ('GWS_user_delete_view', '可以访问删除用户页面'), ('GWS_user_delete_conform', '可以确认删除用户信息'), ('GWS_user_list_view', '可以查看用户列表'))},
        ),
    ]
