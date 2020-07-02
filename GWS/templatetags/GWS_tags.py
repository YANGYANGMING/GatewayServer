from django.template import Library
from django.utils.safestring import mark_safe
from GWS import models


register = Library()


@register.simple_tag
def render_run_time(received_time_data):
    ele = ''
    received_time_data = eval(received_time_data)
    if int(received_time_data['days']):
        ele += '%s天' % received_time_data['days']
    if int(received_time_data['hours']):
        ele += '%s小时' % received_time_data['hours']
    if int(received_time_data['minutes']):
        ele += '%s分钟' % received_time_data['minutes']

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



