# Generated by Django 2.2.2 on 2020-04-16 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GWS', '0009_delete_material'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='material',
            field=models.SmallIntegerField(choices=[(0, '未定义'), (1, '碳钢'), (2, '不锈钢')], default=0),
        ),
    ]
