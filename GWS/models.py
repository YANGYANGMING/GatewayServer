from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class UserProfileManager(BaseUserManager):
    def create_user(self, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not name:
            raise ValueError('Users must have a name')

        user = self.model(
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            password=password,
            name=name,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=64, unique=True,)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.ManyToManyField("Role", blank=True, null=True)
    gateway = models.ManyToManyField('Gateway')

    objects = UserProfileManager()

    USERNAME_FIELD = 'name'

    def get_full_name(self):
        # The user is identified by their email address
        return self.name

    def get_short_name(self):
        # The user is identified by their email address
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ('GWS_manual_config_view', '可以访问配置时间页面'),
            ('GWS_manual_config_get_data_view', '可以手动获取数据'),
            ('GWS_sensor_manage_view', '可以访问传感器管理页面'),
            ('GWS_gateway_manage_view', '可以访问网关管理页面'),
            ('GWS_add_sensor_view', '可以访问增加传感器页面'),
            ('GWS_edit_sensor_view', '可以访问编辑传感器页面'),
            ('GWS_edit_sensor_alarm_msg_view', '可以访问编辑传感器报警信息页面'),
            ('GWS_edit_gateway_view', '可以访问编辑网关页面'),
            ('GWS_resume_sensor_view', '可以开通传感器'),
            ('GWS_pause_sensor_view', '可以禁用传感器'),
            ('GWS_send_server_data_view', '可以对传感器进行增删改操作'),
            ('GWS_set_gateway_json_view', '可以更新网关'),
            ('GWS_user_add_view', '可以访问增加用户页面'),
            ('GWS_user_add_save', '可以保存增加的用户信息'),
            ('GWS_user_edit_view', '可以访问编辑用户页面'),
            ('GWS_user_edit_save', '可以保存编辑的用户信息'),
            ('GWS_user_delete_view', '可以访问删除用户页面'),
            ('GWS_user_delete_conform', '可以确认删除用户信息'),
            ('GWS_user_list_view', '可以查看用户列表'),
        )


class Role(models.Model):
    """角色表"""
    name = models.CharField(max_length=64, unique=True)
    menus = models.ManyToManyField('Menus')

    def __str__(self):
        return self.name


class Menus(models.Model):
    """动态菜单"""
    name = models.CharField(max_length=64)
    url_type_choices = ((0, 'absolute'), (1, 'dynamic'))
    url_type = models.SmallIntegerField(choices=url_type_choices, default=0)
    url_name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'url_name')


class Enterprise(models.Model):
    """
    企业
    """
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Gateway(models.Model):
    """
    网关
    """
    name = models.CharField(max_length=32)
    Enterprise = models.CharField(max_length=128)
    gw_status_choices = ((0, '离线'),
                         (1, '在线'),
                         )
    gw_status = models.SmallIntegerField(choices=gw_status_choices, default=1)
    network_id = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class Material(models.Model):
    """
    材料
    """
    name = models.CharField(max_length=64, unique=True)
    sound_V = models.IntegerField()
    temperature_co = models.FloatField()

    def __str__(self):
        return self.name


class Sensor(models.Model):
    """
    传感器
    """
    sensor_id = models.CharField(max_length=32, unique=True)
    network_id = models.CharField(max_length=32, unique=True)
    alias = models.CharField(max_length=64, null=False, blank=False, unique=True)
    received_time_data = models.CharField(max_length=128)
    battery = models.CharField(max_length=32, default=100)
    cHz = models.CharField(max_length=32, default='2')
    gain = models.CharField(max_length=32, default='60')
    avg_time = models.CharField(max_length=32, default='4')
    Hz = models.CharField(max_length=32, default='2')
    Sample_depth = models.CharField(max_length=32, default='2')
    Sample_Hz = models.CharField(max_length=32, default='500')
    sensor_run_status_choices = ((0, '已禁用'),
                                 (1, '已开通'),
                                 )
    sensor_run_status = models.SmallIntegerField(choices=sensor_run_status_choices, default=1)
    sensor_online_status_choices = ((0, '离线'),
                                    (1, '在线'),
                                    )
    # material_choices = ((0, '未定义'),
    #                     (1, '碳钢'),
    #                     (2, '不锈钢'),
    #                     )
    material = models.SmallIntegerField(default=1)
    sensor_online_status = models.SmallIntegerField(choices=sensor_online_status_choices, default=1)
    sensor_type_choices = ((0, 'ETM-100'),
                           )
    sensor_type = models.SmallIntegerField(choices=sensor_type_choices, default=0)
    Importance_choices = ((0, '一般'),
                          (1, '重要'),
                          )
    Importance = models.SmallIntegerField(choices=Importance_choices, default=0)
    date_of_installation = models.DateField(auto_now_add=True)
    initial_thickness = models.FloatField(default=10)
    alarm_thickness = models.FloatField(default=8)
    alarm_battery = models.FloatField(default=50)
    alarm_temperature = models.FloatField(default=310)
    alarm_corrosion = models.FloatField(default=0.3)
    longitude = models.FloatField(default=0, null=True, blank=True)
    latitude = models.FloatField(default=0, null=True, blank=True)
    area = models.TextField(verbose_name='所在区域', null=True, blank=True)
    location = models.TextField(verbose_name='所在位置', null=True, blank=True)
    location_img_path = models.TextField(verbose_name='所在位置图片路径', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    assembly_crewman = models.CharField(max_length=32, null=True, blank=True)
    delete_status = models.CharField(max_length=32, default=0)
    gateway = models.ForeignKey('Gateway', on_delete=models.CASCADE)

    def __str__(self):
        return self.alias


class Waveforms(models.Model):
    """
    传感器接收到的数据
    """
    network_id = models.ForeignKey(to='Sensor', to_field='network_id', on_delete=models.CASCADE)
    data = models.TextField()
    com_version = models.CharField(max_length=32)
    time_tamp = models.CharField(max_length=32)
    gain = models.CharField(max_length=32)
    temperature = models.IntegerField()
    battery = models.IntegerField()
    data_len = models.IntegerField()
    thickness = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.network_id)


class Corrosion_rate(models.Model):
    """
    腐蚀速率
    """
    sensor = models.ForeignKey('Sensor', on_delete=models.CASCADE)
    corrosion_rate_interval_choices = ((7, '一周'),
                                       (15, '半个月'),
                                       (30, '1个月'),
                                       (90, '3个月'),
                                       (180, '6个月'),
                                       (365, '12个月'),
                                       ('', 'all date'),
                                       )
    corrosion_rate_interval = models.SmallIntegerField(choices=corrosion_rate_interval_choices, default=30)
    corrosion_rate = models.CharField(max_length=32, null=True, blank=True)






