# Generated by Django 2.2.2 on 2020-05-08 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GWS', '0023_auto_20200508_1659'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='Enterprise',
        ),
    ]
