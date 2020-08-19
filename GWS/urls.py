"""GatewayServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path
from GWS.views import views, account

urlpatterns = [
    re_path(r'^index$', views.index),
    re_path(r'^manual-config$', views.manual_config, name="manual_config"),
    re_path(r'^sensor-manage$', views.sensor_manage, name="sensor_manage"),
    re_path(r'^gateway-manage$', views.gateway_manage, name="gateway_manage"),
    re_path(r'^edit-sensor-params$', views.edit_sensor_params, name="edit_sensor_params"),
    re_path(r'^all-data-report$', views.all_data_report),
    re_path(r'^thickness-report$', views.thickness_report),
    re_path(r'^corrosion-rate-list$', views.corrosion_rate_list),
    re_path(r'^add-sensor/(.*)$', views.add_sensor, name="add_sensor"),
    re_path(r'^alarm-sensor-list$', views.alarm_sensor_list),
    re_path(r'^export-data$', views.export_data),

    re_path(r'^user-add$', account.user_add, name="user_add"),
    re_path(r'^user-edit/(\d+)$', account.user_edit, name="user_edit"),
    re_path(r'^user-delete/(\d+)$', account.user_delete, name="user_delete"),
    re_path(r'^user-list$', account.user_list, name="user_list"),
    re_path(r'^user-profile$', account.user_profile),
    re_path(r'^change-pwd$', account.change_pwd),
    re_path(r'^send-sms-verification-code-to-phone$', account.send_sms_verification_code_to_phone),
    re_path(r'^check-role$', account.check_role),

    re_path(r'^data-json-report-(.*)$', views.data_json_report),
    re_path(r'^sensor-data-info-(.*)$', views.sensor_data_info),
    re_path(r'^edit-sensor-(\d+)$', views.edit_sensor, name="edit_sensor"),
    re_path(r'^edit-sensor-alarm-msg-(\d+)$', views.edit_sensor_alarm_msg, name="edit_sensor_alarm_msg"),
    re_path(r'^edit-gateway-(.*)$', views.edit_gateway, name="edit_gateway"),
    re_path(r'^resume-sensor-(\d+)$', views.resume_sensor, name="resume_sensor"),
    re_path(r'^pause-sensor-(\d+)$', views.pause_sensor, name="pause_sensor"),
    re_path(r'^send-server-data$', views.send_server_data, name="send_server_data"),
    re_path(r'^set-gateway-json$', views.set_gateway_json, name="set_gateway_json"),
    re_path(r'^gateway-associated-sensors-json$', views.gateway_associated_sensors_json),
    re_path(r'^set-sensor-params$', views.set_sensor_params, name="set_sensor_params"),

    re_path(r'^show-soundV-json$', views.show_soundV_json),

    re_path(r'^thickness-json-report$', views.thickness_json_report),
    re_path(r'^corrosion-rate-json-report$', views.corrosion_rate_json_report),
    re_path(r'^conform-corrosion-interval-json$', views.conform_corrosion_interval_json),

    re_path(r'^judge-username-exist-json$', views.judge_username_exist_json),
    re_path(r'^judge-sensor-name-exist-json$', views.judge_sensor_name_exist_json),
    re_path(r'^judge-sensor-ntid-exist-json$', views.judge_sensor_ntid_exist_json),
    re_path(r'^judge-sensor-id-exist-json$', views.judge_sensor_id_exist_json),


]
