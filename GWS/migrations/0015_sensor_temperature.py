# Generated by Django 2.2.2 on 2020-04-22 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GWS', '0014_auto_20200422_1006'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='temperature',
            field=models.CharField(default=30, max_length=32),
            preserve_default=False,
        ),
    ]
