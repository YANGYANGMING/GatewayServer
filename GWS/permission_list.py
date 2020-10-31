from GWS import permission_hook

perm_dic = {

    'GWS_manual_config_view': ['manual_config', 'GET', [], {}],  # 可以访问配置时间页面
    'GWS_manual_config_get_data_view': ['manual_config', 'POST', [], {}],  # 可以手动取数
    'GWS_sensor_manage_view': ['sensor_manage', 'GET', [], {}],  # 可以访问传感器管理页面
    'GWS_gateway_manage_view': ['gateway_manage', 'GET', [], {}],  # 可以访问网关管理页面
    'GWS_add_sensor_view': ['add_sensor', 'GET', [], {}],  # 可以访问增加传感器页面
    'GWS_edit_sensor_view': ['edit_sensor', 'GET', [], {}],  # 可以访问编辑传感器页面
    'GWS_edit_sensor_alarm_msg_view': ['edit_sensor_alarm_msg', 'GET', [], {}],  # 可以访问编辑传感器报警信息页面
    'GWS_edit_gateway_view': ['edit_gateway', 'GET', [], {}],  # 可以访问编辑网关页面
    'GWS_resume_sensor_view': ['resume_sensor', 'GET', [], {}],  # 可以开通传感器
    'GWS_pause_sensor_view': ['pause_sensor', 'GET', [], {}],  # 可以禁用传感器
    'GWS_send_server_data_view': ['send_server_data', 'POST', [], {}],  # 可以对传感器进行增删改操作
    'GWS_set_gateway_json_view': ['set_gateway_json', 'POST', [], {}],  # 可以更新网关
    'GWS_edit_sensor_params_view': ['edit_sensor_params', 'GET', [], {}],  # 可以访问传感器参数页面
    'GWS_set_sensor_params_view': ['set_sensor_params', 'POST', [], {}],  # 可以设置传感器参数
    'GWS_export_data_view': ['export_data', 'GET', [], {}],  # 可以访问导出数据页面
    'GWS_system_settings_view': ['system_settings', 'GET', [], {}],  # 可以访问系统设置页面
    'GWS_control_upload_data_view': ['control_upload_data', 'GET', [], {}],  # 可以设置上传数据到特检局

    'GWS_user_add_view': ['user_add', 'GET', [], {}],  # 可以访问增加用户页面
    'GWS_user_add_save': ['user_add', 'POST', [], {}],  # 可以保存增加的用户信息
    'GWS_user_edit_view': ['user_edit', 'GET', [], {}],  # 可以访问编辑用户页面
    'GWS_user_edit_save': ['user_edit', 'POST', [], {}],  # 可以保存编辑的用户信息
    'GWS_user_delete_view': ['user_delete', 'GET', [], {}],  # 可以访问删除用户页面
    'GWS_user_delete_conform': ['user_delete', 'POST', [], {}],  # 可以确认删除用户信息
    'GWS_user_list_view': ['user_list', 'GET', [], {}],  # 可以查看用户列表

}
