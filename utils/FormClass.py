from django import forms
from django.forms import fields
from django.forms import widgets as wid
from django.forms import ModelForm
from GWS import models

class DataForm(forms.Form):
    url = fields.URLField(
        required=False,
        widget=wid.Input(attrs={'class': 'form-control', 'placeholder': 'http://ling.2tag.cn/api/collect_data'})
    )


class ChangepwdForm(forms.Form):
    old_pwd = fields.CharField(label='旧密码', max_length=32, widget=wid.PasswordInput(attrs={'class': 'form-control'}))
    new_pwd = fields.CharField(label='新密码', max_length=32, widget=wid.PasswordInput(attrs={'class': 'form-control'}))
    new_pwd_confirm = fields.CharField(label='重复新密码', max_length=32, widget=wid.PasswordInput(attrs={'class': 'form-control'}))


class UserEditForm(ModelForm):
    class Meta:
        model = models.UserProfile  # 对应的Model中的类
        fields = '__all__'      # 字段，如果是'__all__',就是表示列出所有的字段
        exclude = ['is_superuser', 'is_staff', 'password', 'last_login']          # 排除的字段
        help_texts = None       # 帮助提示信息
        error_messages = None   # 自定义错误信息
        # widgets用法
        widgets = {
            "name": wid.Input(attrs={'class': 'form-control', 'style': 'width: 50%'}),
            "role": wid.SelectMultiple(attrs={'class': 'form-control', 'style': 'width: 50%;'}),
            "gateway": wid.SelectMultiple(attrs={'class': 'form-control', 'style': 'width: 50%;'}),
            "user_permissions": wid.SelectMultiple(attrs={'class': 'form-control', 'style': 'width: 50%; height: 150px'}),
            "groups": wid.SelectMultiple(attrs={'class': 'form-control', 'style': 'width: 50%;'}),
        }
        labels = {
            'name': '用户名',
            'role': '角色',
            'gateway': '网关',
            'is_active': '可以登录',
        }


class UserAddForm(ModelForm):
    class Meta:
        model = models.UserProfile  # 对应的Model中的类
        fields = '__all__'      # 字段，如果是'__all__',就是表示列出所有的字段
        exclude = ['is_superuser', 'is_staff', 'last_login']          # 排除的字段
        help_texts = None       # 帮助提示信息
        error_messages = None   # 自定义错误信息
        # widgets用法
        widgets = {
            "password": wid.Input(attrs={'class': 'form-control', 'style': 'width: 50%'}),
            "name": wid.Input(attrs={'class': 'form-control', 'style': 'width: 50%'}),
            "role": wid.SelectMultiple(attrs={'class': 'form-control', 'style': 'width: 50%;'}),
            "gateway": wid.SelectMultiple(attrs={'class': 'form-control', 'style': 'width: 50%;'}),
            "user_permissions": wid.SelectMultiple(attrs={'class': 'form-control', 'style': 'width: 50%; height: 150px'}),
            "groups": wid.SelectMultiple(attrs={'class': 'form-control', 'style': 'width: 50%;'}),
        }
        labels = {
            'name': '用户名',
            'role': '角色',
            'gateway': '网关',
            'is_active': '可以登录',
        }
