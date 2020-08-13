from django.shortcuts import render, redirect, HttpResponsefrom django.contrib.auth import authenticate, login, logoutfrom django.contrib.auth.hashers import make_passwordfrom django.contrib.auth.decorators import login_requiredfrom django.views.decorators.csrf import csrf_exemptfrom django.contrib.auth.models import Groupfrom django.core.cache import cachefrom utils.handle_func import judge_user_idfrom utils.FormClass import *from utils.check_click_method import check_click_methodfrom utils import handle_funcfrom utils.SDKCore import send_smsfrom GWS import modelsfrom GWS import permissionsfrom GWS.views.views import logimport randomimport json@csrf_exemptdef acc_login(request):    """登录"""    result = {'status': False, 'msg': ''}    if request.method == "POST":        username = request.POST.get('username')        password = request.POST.get('password')        rmb = request.POST.get('rmb')        role_obj = models.UserProfile.objects.values('role__name').filter(name=username)        if role_obj:            role = role_obj[0]['role__name']        else:            role = None        # 手机验证码验证        if role == "超级管理员" or role == "用户管理员":            sms_code = request.POST.get('sms_code')            if sms_code == cache.get('sms_code'):                sms_verification_code_conform = True            else:                sms_verification_code_conform = False        else:            sms_verification_code_conform = True        sms_verification_code_conform = True        user = authenticate(username=username, password=password)        if user and sms_verification_code_conform:            print("passed authentication")            login(request, user)  # 把user封装到request.session中            if rmb:                request.session.set_expiry(60 * 60 * 24 * 7)                print('rmb')                result = {'status': True, 'msg': '登陆成功'}                # Log                log.log(result['status'], result['msg'], user=str(request.user))            return redirect('/GWS/index')  # 登录后跳转至next指定的页面，否则到首页        else:            result['msg'] = "用户名或密码错误!"            # Log            log.log(result['status'], result['msg'], user=str(request.user))    return render(request, 'login.html', locals())@csrf_exemptdef send_sms_verification_code_to_phone(request):    """    发送短信验证码到手机    :param request:    :return:    """    PhoneNumbers = request.POST.get('PhoneNumbers')    sms_code = random.randrange(10000, 99999)    # 把生成的验证码放入缓存，5分钟后过期    cache.set('sms_code', str(sms_code), 60 * 5)    sms_response = {}    try:        sms_response = send_sms(PhoneNumbers, sms_code)        print(type(sms_response))        print(sms_response)    except Exception as e:        sms_response['status'] = False        print(e)    if sms_response == "OK":        sms_response['status'] = True    else:        sms_response['status'] = False    log.log(sms_response['status'], sms_response["Message"])    return HttpResponse(json.dumps(sms_response))def check_role(request):    """    检查登录用户的角色    :param request:    :return:    """    username = request.GET.get('username')    role = models.UserProfile.objects.values('role__name').filter(name=username)    if role:        role_name = role[0]['role__name']    else:        role_name = ""    return HttpResponse(json.dumps(role_name))def acc_logout(request):    """退出"""    # request.session.clear()    result = {'status': True, 'msg': '退出成功'}    # Log    log.log(result['status'], result['msg'], user=str(request.user))    logout(request)    return redirect('/login/')def page_404(request):    """404页面"""    return render(request, '404.html')@permissions.check_permission@login_requireddef user_add(request):    """    增加用户    :param request:    :return:    """    user_obj = models.UserProfile.objects.get(id=request.user.id)    if request.method == "GET":        roles_obj = models.Role.objects.values('id', 'name').all().exclude(name__in=['超级管理员', '用户管理员'])        groups_obj = Group.objects.values('id', 'name').all().exclude(name='超级管理员权限')        cur_role_list = [item['name'] for item in models.UserProfile.objects.get(id=request.user.id).role.values('name')]        if '超级管理员' in cur_role_list or '用户管理员' in cur_role_list:            gateway_obj = models.Gateway.objects.all().values('id', 'name').exclude(name='零声科技')        else:            gateway_obj = models.UserProfile.objects.get(id=request.user.id).gateway.values('id', 'name')        return render(request, "GWS/user_add.html", locals())    elif request.method == "POST":        name = request.POST.get('name')        if name == "" or request.POST.get('password') == "":            return redirect('/GWS/user-add')        password = make_password(request.POST.get('password'))        role = request.POST.getlist('role')        gateway = request.POST.getlist('gateway')        groups = request.POST.getlist('groups')        # user_permissions = request.POST.getlist('user_permissions')        is_active = False if not request.POST.get('is_active') else True        # create user        try:            create_user_obj = models.UserProfile.objects.create(name=name, password=password, is_active=is_active)            create_user_obj.role.add(*role)            create_user_obj.gateway.add(*gateway)            create_user_obj.groups.add(*groups)            # create_user_obj.user_permissions.add(*user_permissions)        except Exception as e:            print(e)        return redirect('/GWS/user-list')@csrf_exempt@permissions.check_permission@login_required@check_click_methoddef user_edit(request, nid):    """    编辑用户    :param request:    :return:    """    nid = int(nid)    # 防止在开发者模式下修改url    user_id_conform = judge_user_id(request, nid)    if not user_id_conform:        return redirect('/GWS/user-list')    user_obj = models.UserProfile.objects.filter(id=nid)    if request.method == "GET":        # 在编辑用户页面显示选中的用户权限        cur_user_all_permissions_list, selected_user_permissions_list = handle_func.show_selected_permissions(request, Group, nid)        # 用于超级用户给企业用户分配网关        cur_role_list = [item['name'] for item in models.UserProfile.objects.get(id=request.user.id).role.values('name')]        if '超级管理员' in cur_role_list or '用户管理员' in cur_role_list:            gateway_obj = models.Gateway.objects.all().values('id', 'name')        else:            gateway_obj = models.UserProfile.objects.get(id=request.user.id).gateway.values('id', 'name')        roles_obj = models.Role.objects.values('id', 'name').exclude(name__in=['超级管理员', '用户管理员'])        groups_obj = Group.objects.values('id', 'name').exclude(name='超级管理员权限')        cur_name = user_obj.values('name')[0]['name']        cur_role = user_obj[0].role.values('id').all()        role_list = [item['id'] for item in cur_role]        cur_gateway = user_obj[0].gateway.values('id').all()        gateway_list = [item['id'] for item in cur_gateway]        cur_group = user_obj[0].groups.values('id').all()        group_list = [item['id'] for item in cur_group]        is_active = user_obj.values('is_active')[0]['is_active']        return render(request, "GWS/user_edit.html", locals())    elif request.method == "POST":        name = request.POST.get('name')        role = request.POST.getlist('role')        gateway = request.POST.getlist('gateway')        groups = request.POST.getlist('groups')        user_permissions = request.POST.getlist('user_permissions')        is_active = False if not request.POST.get('is_active') else True        # update user        try:            user_obj.update(name=name, is_active=is_active)            user_obj[0].role.set(role)            user_obj[0].gateway.set(gateway)            user_obj[0].groups.set(groups)            user_obj[0].user_permissions.set(user_permissions)        except Exception as e:            print(e)        return redirect('/GWS/user-list')@csrf_exempt@permissions.check_permission@login_required@check_click_methoddef user_delete(request, nid):    """    删除用户确认页    :param request:    :param nid: 用户id    :return:    """    obj = models.UserProfile.objects.get(id=nid)    role = obj.role.values('name')[0]['name']    if request.method == "POST":        obj.delete()        return redirect("/GWS/user-list")    return render(request, "GWS/user_delete.html", locals())@permissions.check_permission@login_requireddef user_list(request):    """    用户列表    :param request:    :return:    """    try:        cur_user_obj = models.UserProfile.objects.filter(id=request.user.id)        cur_user_roles = cur_user_obj[0].role.values('name')        cur_user_role_list = [item['name'] for item in cur_user_roles]        cur_user_enterprise = cur_user_obj[0].gateway.values('Enterprise')[0]['Enterprise']        if '超级管理员' in cur_user_role_list or '用户管理员' in cur_user_role_list:  # 如果是超级管理员，可以查看修改所有用户信息            user_list = models.UserProfile.objects.all().values('id',                                                                'is_active',                                                                'role__name',                                                                'name',                                                                'gateway__Enterprise',                                                                'last_login').distinct()        else:            user_list = models.UserProfile.objects.filter(gateway__Enterprise=cur_user_enterprise). \                values('id', 'is_active', 'name', 'role__name', 'gateway__Enterprise', 'last_login').distinct()    except Exception as e:        print(e)    return render(request, "GWS/user_list.html", locals())@csrf_exempt@login_requireddef user_profile(request):    """    查看修改个人信息    :param request:    :return:    """    obj = models.UserProfile.objects.values('name', 'role__name', 'last_login').get(id=request.user.id)    if request.method == "POST":        name = request.POST.get('name')        models.UserProfile.objects.filter(name=obj['name']).update(name=name)        obj = models.UserProfile.objects.values('name', 'role__name', 'last_login').get(id=request.user.id)    return render(request, 'GWS/userprofile.html', locals())@csrf_exempt@login_requireddef change_pwd(request):    """修改密码"""    result = {'message': ''}    form = ChangepwdForm()    if not request.user.is_authenticated:        result['message'] = '未登录'        print('未登录')        return render(request, 'GWS/change_pwd.html', locals())    elif request.method == "POST":        form = ChangepwdForm(request.POST)        if form.is_valid():            old_pwd = form.cleaned_data['old_pwd']            new_pwd = form.cleaned_data['new_pwd']            new_pwd_confirm = form.cleaned_data['new_pwd_confirm']            user = authenticate(username=request.user, password=old_pwd)            if user: #旧密码正确                if new_pwd == new_pwd_confirm: #两次新密码一致                    user.set_password(new_pwd)                    user.save()                    print('更改成功')                    return redirect('logout')                else: #两次新密码不一致                    result['message'] = '两次密码不一致'                    return render(request, 'GWS/change_pwd.html', locals())            else:                result['message'] = '旧密码错误'                return render(request, 'GWS/change_pwd.html', locals())    return render(request, 'GWS/change_pwd.html', locals())