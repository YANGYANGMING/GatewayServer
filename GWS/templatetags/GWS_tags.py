from django.template import Library
from django.utils.safestring import mark_safe
from GWS import models


register = Library()


@register.simple_tag
def render_run_time(received_time_data):
    ele = ''
    received_time_data = eval(received_time_data)
    if received_time_data['month'] == '*':
        ele += '每月-'
    else:
        ele += '%s月-' % received_time_data['month']
    if received_time_data['day'] == '*':
        ele += '每日-'
    else:
        ele += '%s日-' % received_time_data['day']
    if received_time_data['hour'] == '*':
        ele += '每小时-'
    else:
        ele += '%s点-' % received_time_data['hour']
    if received_time_data['mins'] == '*':
        ele += '每分钟-'
    else:
        ele += '%s分整' % received_time_data['mins']

    return mark_safe(ele)


@register.simple_tag
def render_menus_tree(request):
    """
    生成左侧菜单树
    :param request:
    :return:
    """
    ele = ''
    try:
        user_obj = models.UserProfile.objects.filter(name=request.user).first()
        role_list = user_obj.role.all()
        menus_obj_list = []
        for item in role_list:
            menus_obj_list += item.menus.all()
        menus_obj_list = list(set(menus_obj_list))
        for menu in menus_obj_list:
            if request.path == menu.url_name:
                ele += '<li class="active">'
            else:
                ele += '<li>'
            if menu.url_type == 0:
                ele += """<a href="%s"><span>%s </span></a></li>""" % (menu.url_name, menu.name)
            elif menu.url_type == 1 and menu.url_name == 'add_sensor':
                ele += """<a href="/GWS/add-sensor/new"><span>%s </span></a></li>""" % (menu.name)
    except Exception as e:
        print(e)

    return mark_safe(ele)



